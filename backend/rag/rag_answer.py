
import os
import re

import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer


# -----------------------------
# Load environment variables
# -----------------------------

load_dotenv("backend/.env", override=True)


# -----------------------------
# 1. Load local embedding model
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# 2. Connect to ChromaDB
# -----------------------------

client = chromadb.PersistentClient(
    path="backend/rag/chroma_db"
)

collection = client.get_collection(
    name="tax_rules"
)


# -----------------------------
# 3. Connect to OpenRouter
# -----------------------------



api_key = os.getenv("OPENROUTER_API_KEY")

llm_client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)


# -----------------------------
# 4. Retrieve tax rules
# -----------------------------

def retrieve_rules(question):

    question_embedding = model.encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=7
    )

    return results["documents"][0]


# -----------------------------
# 5. Find matching income rule
# -----------------------------

def find_matching_rule(question, documents):

    question = question.lower()

    # Example: 7 lakh or 7.5 lakh
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:lakh|lakhs)",
        question
    )

    if match:

        income = float(match.group(1)) * 100000

    else:

        # Example: 700000 or 900000
        match = re.search(
            r"\b\d{5,}\b",
            question
        )

        if match:

            income = float(match.group(0))

        else:

            return None


    # Check every retrieved rule

    for document in documents:

        numbers = re.findall(
            r"\d+",
            document
        )

        numbers = [
            int(number)
            for number in numbers
        ]


        # Remove Rule number

        if numbers:
            numbers = numbers[1:]


        # Example:
        # Annual income up to 400000

        if "up to" in document.lower():

            maximum = numbers[0]

            if income <= maximum:
                return document


        # Example:
        # Annual income above 2000000

        elif "above" in document.lower():

            minimum = numbers[0]

            if income > minimum:
                return document


        # Example:
        # 400001 to 800000

        elif len(numbers) >= 2:

            minimum = numbers[0]
            maximum = numbers[1]

            if minimum <= income <= maximum:
                return document


    return None


# -----------------------------
# 6. Generate answer using OpenRouter
# -----------------------------

def generate_answer(question, tax_rule):

    prompt = f"""
You are a tax assistant.

Answer the user's question using ONLY the tax rule below.

Tax rule:
{tax_rule}

User question:
{question}

Do not invent any additional tax rules.

Give a short and clear answer.
"""


    response = llm_client.chat.completions.create(

        model="openai/gpt-4o-mini",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response.choices[0].message.content


# -----------------------------
# 7. Main program
# -----------------------------

if __name__ == "__main__":

    question = input(
        "Ask a tax question: "
    )

    # Retrieve rules
    documents = retrieve_rules(question)

    # Find correct numerical rule
    tax_rule = find_matching_rule(
        question,
        documents
    )

    print("\nRetrieved tax rule:")

    if tax_rule:

        print(tax_rule)

        # Ask OpenRouter LLM
        answer = generate_answer(
            question,
            tax_rule
        )

        print("\nAI Answer:")
        print(answer)

    else:

        print(
            "No matching tax rule found."
        )
