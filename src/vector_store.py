import os
import uuid
import yaml
import chromadb

from chromadb.config import Settings
from chromadb.utils import embedding_functions


class VectorStore:

    def __init__(self):

        # ----------------------------------------
        # PROJECT ROOT PATH
        # ----------------------------------------
        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        persist_path = os.path.join(base_dir, "chroma_db")

        print("Chroma persist path:", persist_path)

        # ----------------------------------------
        # PERSISTENT CHROMADB CLIENT
        # ----------------------------------------
        self.client = chromadb.Client(
            Settings(
                persist_directory=persist_path,
                is_persistent=True
            )
        )

        # ----------------------------------------
        # EMBEDDING MODEL
        # ----------------------------------------
        # Converts text → vector embeddings
        # Used for semantic similarity search
        # ----------------------------------------
        self.embedding_function = (
            embedding_functions
            .SentenceTransformerEmbeddingFunction(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        )

        # ----------------------------------------
        # CREATE / LOAD COLLECTION
        # ----------------------------------------
        self.collection = self.client.get_or_create_collection(
            name="qa_collection",
            embedding_function=self.embedding_function
        )

        print(
            "Collection document count:",
            self.collection.count()
        )

    # ============================================
    # ADD SINGLE DOCUMENT
    # ============================================
    def add_document(self, document: str, metadata: dict):

        """
        Adds a single document chunk into ChromaDB.
        """

        # ----------------------------------------
        # PREVENT EMPTY METADATA
        # ----------------------------------------
        if not metadata:
            metadata = {
                "source": "unknown"
            }

        try:
            self.collection.add(
                documents=[document],
                metadatas=[metadata],
                ids=[str(uuid.uuid4())]
            )

        except Exception as e:
            print("Error adding document:", e)

    # ============================================
    # LOAD DOCUMENTS FROM qa_data FOLDER
    # ============================================
    def load_documents_from_folder(self, folder_path: str):

        """
        Loads all markdown QA files into ChromaDB.

        Features:
        - Clears old embeddings
        - Extracts metadata
        - Chunks text
        - Stores embeddings
        """

        print("Loading documents from:", folder_path)

        # ----------------------------------------
        # CLEAR EXISTING COLLECTION
        # ----------------------------------------
        current_count = self.collection.count()

        if current_count > 0:

            print(
                f"Clearing existing collection "
                f"({current_count} documents)..."
            )

            try:
                all_docs = self.collection.get()

                if all_docs["ids"]:
                    self.collection.delete(
                        ids=all_docs["ids"]
                    )

                print("Collection cleared.")

            except Exception as e:
                print("Error clearing collection:", e)

        # ----------------------------------------
        # TRACK TOTAL CHUNKS
        # ----------------------------------------
        total_chunks_added = 0

        # ----------------------------------------
        # WALK THROUGH qa_data FOLDER
        # ----------------------------------------
        for root, _, files in os.walk(folder_path):

            for file in files:

                if file.endswith(".md"):

                    full_path = os.path.join(root, file)

                    print("Processing:", file)

                    try:

                        with open(
                            full_path,
                            "r",
                            encoding="utf-8"
                        ) as f:

                            content = f.read()

                            # --------------------
                            # EXTRACT METADATA
                            # --------------------
                            metadata, body = (
                                self._extract_metadata(content)
                            )

                            # Add source filename
                            metadata["file_name"] = file

                            # --------------------
                            # CHUNK DOCUMENT
                            # --------------------
                            chunks = self._chunk_text(body)

                            # --------------------
                            # STORE CHUNKS
                            # --------------------
                            for chunk in chunks:

                                if chunk.strip():

                                    self.add_document(
                                        chunk,
                                        metadata
                                    )

                                    total_chunks_added += 1

                    except Exception as e:
                        print(
                            f"Error processing {file}:",
                            e
                        )

        # ----------------------------------------
        # FINAL DB STATS
        # ----------------------------------------
        final_count = self.collection.count()

        print(f"Total chunks added: {total_chunks_added}")

        print(
            f"Final document count in DB: "
            f"{final_count}"
        )

        print(
            "QA knowledge base successfully refreshed."
        )

    # ============================================
    # VECTOR SEARCH
    # ============================================
    def search(
        self,
        query: str,
        top_k: int = 5,
        where: dict = None
    ):

        """
        Performs semantic similarity search.

        Returns:
        [
            {
                "document": "...",
                "confidence": 91.4
            }
        ]
        """

        print(
            "Searching DB... Total docs:",
            self.collection.count()
        )

        try:

            # ------------------------------------
            # QUERY CHROMADB
            # ------------------------------------
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

            # ------------------------------------
            # HANDLE EMPTY RESULTS
            # ------------------------------------
            if not results.get("documents"):
                return []

            documents = results["documents"][0]

            distances = results.get(
                "distances",
                [[]]
            )[0]

            scored_results = []

            # ------------------------------------
            # CONVERT DISTANCE → CONFIDENCE
            # ------------------------------------
            for doc, distance in zip(
                documents,
                distances
            ):

                # Smaller distance = better match
                similarity = max(0, 1 - distance)

                confidence = round(
                    similarity * 100,
                    2
                )

                scored_results.append({
                    "document": doc,
                    "confidence": confidence
                })

            return scored_results

        except Exception as e:

            print("Search error:", e)

            return []

    # ============================================
    # EXTRACT YAML METADATA
    # ============================================
    def _extract_metadata(self, content: str):

        """
        Extract YAML front matter metadata.
        """

        metadata = {}
        body = content

        if content.startswith("---"):

            try:

                parts = content.split("---", 2)

                metadata = yaml.safe_load(
                    parts[1]
                ) or {}

                body = parts[2]

            except Exception as e:

                print(
                    "Metadata parsing error:",
                    e
                )

                metadata = {}

        # ----------------------------------------
        # CLEAN METADATA TYPES
        # ----------------------------------------
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

    # ============================================
    # TEXT CHUNKING
    # ============================================
    def _chunk_text(
        self,
        text: str,
        chunk_size: int = 800
    ):

        """
        Splits large documents into
        smaller semantic chunks.
        """

        paragraphs = text.split("\n\n")

        chunks = []

        current_chunk = ""

        for para in paragraphs:

            if (
                len(current_chunk) + len(para)
                < chunk_size
            ):

                current_chunk += para + "\n\n"

            else:

                chunks.append(
                    current_chunk.strip()
                )

                current_chunk = para + "\n\n"

        if current_chunk:

            chunks.append(
                current_chunk.strip()
            )

        return chunks