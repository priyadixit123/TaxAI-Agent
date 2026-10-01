from langchain_text_splitters import RecursiveCharacterTextSplitter


with open("backend/documents/tax_rules.txt", "r") as file:
    text = file.read()


splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20
)


chunks = splitter.split_text(text)


print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print("\nCHUNK", i + 1)
    print(chunk)