import os
import uuid
import yaml
import chromadb

from chromadb.config import Settings
from chromadb.utils import embedding_functions


class VectorStore:

    def __init__(self):

        # ============================================
        # PROJECT ROOT PATH
        # ============================================
        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        persist_path = os.path.join(
            base_dir,
            "chroma_db"
        )

        print(f"Chroma persist path: {persist_path}")

        # ============================================
        # INITIALIZE CHROMADB CLIENT
        # ============================================
        self.client = chromadb.Client(
            Settings(
                persist_directory=persist_path,
                is_persistent=True
            )
        )

        # ============================================
        # EMBEDDING MODEL
        # ============================================
        self.embedding_function = (
            embedding_functions
            .SentenceTransformerEmbeddingFunction(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        )

        # ============================================
        # CREATE / LOAD COLLECTION
        # ============================================
        self.collection = (
            self.client.get_or_create_collection(
                name="qa_collection",
                embedding_function=self.embedding_function
            )
        )

        print(
            "Collection document count:",
            self.collection.count()
        )

    # =====================================================
    # ADD DOCUMENT
    # =====================================================
    def add_document(
        self,
        document: str,
        metadata: dict = None,
        document_id: str = None
    ):

        """
        Add semantic chunk into ChromaDB.
        """

        # ----------------------------------------
        # VALIDATE DOCUMENT
        # ----------------------------------------
        if not document or not document.strip():
            print("Skipping empty document")
            return

        # ----------------------------------------
        # DEFAULT METADATA
        # ----------------------------------------
        if not metadata:
            metadata = {
                "source": "unknown"
            }

        # ----------------------------------------
        # GENERATE ID
        # ----------------------------------------
        if not document_id:
            document_id = str(uuid.uuid4())

        try:

            # ----------------------------------------
            # PREVENT DUPLICATES
            # ----------------------------------------
            existing = self.collection.get(
                ids=[document_id]
            )

            if existing and existing.get("ids"):
                print(
                    f"Skipping duplicate document: "
                    f"{document_id}"
                )
                return

            # ----------------------------------------
            # STORE EMBEDDING
            # ----------------------------------------
            self.collection.add(
                documents=[document],
                metadatas=[metadata],
                ids=[document_id]
            )

            print(
                f"Document added: {document_id}"
            )

        except Exception as e:

            print(
                "Error adding document:",
                e
            )

    # =====================================================
    # LOAD DOCUMENTS
    # =====================================================
    def load_documents_from_folder(
        self,
        folder_path: str
    ):

        """
        Loads markdown QA documents,
        chunks them,
        and stores embeddings.
        """

        print(
            f"\nLoading documents from: {folder_path}"
        )

        total_chunks_added = 0

        # ============================================
        # WALK THROUGH FILES
        # ============================================
        for root, _, files in os.walk(folder_path):

            for file in files:

                if not file.endswith(".md"):
                    continue

                full_path = os.path.join(
                    root,
                    file
                )

                print(f"\nProcessing: {file}")

                try:

                    with open(
                        full_path,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        content = f.read()

                    # --------------------------------
                    # EXTRACT METADATA
                    # --------------------------------
                    metadata, body = (
                        self._extract_metadata(
                            content
                        )
                    )

                    metadata["file_name"] = file

                    # --------------------------------
                    # CHUNK DOCUMENT
                    # --------------------------------
                    chunks = self._chunk_text(
                        body
                    )

                    print(
                        f"Generated {len(chunks)} chunks"
                    )

                    # --------------------------------
                    # STORE CHUNKS
                    # --------------------------------
                    for index, chunk in enumerate(chunks):

                        if not chunk.strip():
                            continue

                        chunk_id = (
                            f"{file}_{index}"
                        )

                        chunk_metadata = {
                            **metadata,
                            "chunk_index": index
                        }

                        self.add_document(
                            document=chunk,
                            metadata=chunk_metadata,
                            document_id=chunk_id
                        )

                        total_chunks_added += 1

                except Exception as e:

                    print(
                        f"Error processing {file}:",
                        e
                    )

        print(
            f"\nTotal chunks added: "
            f"{total_chunks_added}"
        )

        print(
            f"Final DB document count: "
            f"{self.collection.count()}"
        )

        print(
            "\nQA knowledge base loaded successfully."
        )

    # =====================================================
    # VECTOR SEARCH
    # =====================================================
    def search(
        self,
        query: str,
        top_k: int = 5,
        where: dict = None
    ):

        """
        Semantic similarity search.

        Returns:
        {
            documents,
            distances,
            metadatas
        }
        """

        print(
            f"\nSearching vector DB..."
        )

        print(
            f"Total documents: "
            f"{self.collection.count()}"
        )

        try:

            # ========================================
            # QUERY CHROMADB
            # ========================================
            if where:

                results = self.collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    where=where
                )

            else:

                results = self.collection.query(
                    query_texts=[query],
                    n_results=top_k
                )

            # ========================================
            # HANDLE EMPTY RESULTS
            # ========================================
            if not results.get("documents"):

                print(
                    "No matching documents found."
                )

                return {
                    "documents": [],
                    "distances": [],
                    "metadatas": []
                }

            # ========================================
            # DEBUG RESULTS
            # ========================================
            docs = results["documents"][0]

            distances = results.get(
                "distances",
                [[]]
            )[0]

            print("\nTop semantic matches:")

            for i, (doc, dist) in enumerate(
                zip(docs, distances)
            ):

                confidence = round(
                    max(
                        0,
                        min(
                            100,
                            (1 - dist) * 100
                        )
                    ),
                    2
                )

                preview = (
                    doc[:120]
                    .replace("\n", " ")
                )

                print(
                    f"{i+1}. "
                    f"Confidence={confidence}% "
                    f"| Distance={round(dist, 4)}"
                )

                print(
                    f"Preview: {preview}"
                )

                print("-" * 50)

            # ========================================
            # RETURN RAW RESULTS
            # ========================================
            return {
                "documents": results.get(
                    "documents",
                    []
                ),
                "distances": results.get(
                    "distances",
                    []
                ),
                "metadatas": results.get(
                    "metadatas",
                    []
                )
            }

        except Exception as e:

            print(
                "Search error:",
                e
            )

            return {
                "documents": [],
                "distances": [],
                "metadatas": []
            }

    # =====================================================
    # EXTRACT YAML METADATA
    # =====================================================
    def _extract_metadata(
        self,
        content: str
    ):

        metadata = {}
        body = content

        if content.startswith("---"):

            try:

                parts = content.split(
                    "---",
                    2
                )

                metadata = (
                    yaml.safe_load(
                        parts[1]
                    ) or {}
                )

                body = parts[2]

            except Exception as e:

                print(
                    "Metadata parsing error:",
                    e
                )

                metadata = {}

        # ============================================
        # CLEAN METADATA TYPES
        # ============================================
        cleaned_metadata = {}

        for key, value in metadata.items():

            if isinstance(
                value,
                (str, int, float, bool)
            ):

                cleaned_metadata[key] = value

            else:

                cleaned_metadata[key] = str(value)

        return cleaned_metadata, body

    # =====================================================
    # TEXT CHUNKING
    # =====================================================
    def _chunk_text(
        self,
        text: str,
        chunk_size: int = 500
    ):

        """
        Split documents into
        semantic chunks for better RAG retrieval.
        """

        paragraphs = text.split("\n\n")

        chunks = []

        current_chunk = ""

        for para in paragraphs:

            para = para.strip()

            if not para:
                continue

            # ----------------------------------------
            # BUILD CHUNK
            # ----------------------------------------
            if (
                len(current_chunk) + len(para)
                < chunk_size
            ):

                current_chunk += (
                    para + "\n\n"
                )

            else:

                chunks.append(
                    current_chunk.strip()
                )

                current_chunk = (
                    para + "\n\n"
                )

        # ============================================
        # FINAL CHUNK
        # ============================================
        if current_chunk.strip():

            chunks.append(
                current_chunk.strip()
            )

        return chunks