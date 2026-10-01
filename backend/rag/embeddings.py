from sentence_transformers import SentenceTransformer
import chromadb


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Read tax rules
with open("backend/documents/tax_rules.txt", "r") as file:
    text = file.read()


# Simple chunks
chunks = [
    chunk.strip()
    for chunk in text.split("\n\n")
    if chunk.strip()
]


# Create ChromaDB
client = chromadb.PersistentClient(
    path="backend/rag/chroma_db"
)


# Create collection
collection = client.get_or_create_collection(
    name="tax_rules"
)


# Create embeddings
embeddings = model.encode(chunks).tolist()


# Store chunks
collection.add(
    ids=[f"rule_{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings
)


print("Tax rules stored successfully!")
print("Total chunks:", len(chunks))