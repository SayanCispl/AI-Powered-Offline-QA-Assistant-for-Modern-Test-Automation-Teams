import os
from src.vector_store import VectorStore

DATA_DIR = "data/qa_data"

def load_documents():
    docs = []

    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)

                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                docs.append({
                    "id": file,
                    "text": content,
                    "source": path
                })

    return docs


def main():
    vector_store = VectorStore()

    documents = load_documents()

    print(f"Found {len(documents)} documents")

    for doc in documents:
        vector_store.add_document(
            document=doc["text"],
            metadata={"source": doc["source"]},
            document_id=doc["id"]
        )

    print("Embeddings loaded successfully")


if __name__ == "__main__":
    main()