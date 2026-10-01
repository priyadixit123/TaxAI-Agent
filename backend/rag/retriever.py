from sentence_transformers import SentenceTransformer
import chromadb
import re


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to ChromaDB
client = chromadb.PersistentClient(
    path="backend/rag/chroma_db"
)

collection = client.get_collection(
    name="tax_rules"
)


def extract_income(question):

    question = question.lower()

    # Example: 7 lakh / 7.5 lakh
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:lakh|lakhs)",
        question
    )

    if match:
        return float(match.group(1)) * 100000

    # Example: 900000 / 700000
    match = re.search(
        r"\b\d{5,}\b",
        question
    )

    if match:
        return float(match.group(0))

    return None


question = input("Ask a tax question: ")

income = extract_income(question)

print("\nIncome detected:", income)


# Convert question into embedding
question_embedding = model.encode(question).tolist()


# Search ChromaDB
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=7
)

documents = results["documents"][0]


print("\nRelevant tax rules:\n")


if income is not None:

    for document in documents:

        numbers = re.findall(r"\d+", document)

        numbers = [int(number) for number in numbers]

        # Remove Rule number
        if numbers:
            numbers = numbers[1:]

        if "up to" in document.lower():

            maximum = numbers[0]

            if income <= maximum:
                print(document)
                break

        elif "above" in document.lower():

            minimum = numbers[0]

            if income > minimum:
                print(document)
                break

        elif len(numbers) >= 2:

            minimum = numbers[0]
            maximum = numbers[1]

            if minimum <= income <= maximum:
                print(document)
                break

else:

    for document in documents[:2]:

        print(document)
        print()