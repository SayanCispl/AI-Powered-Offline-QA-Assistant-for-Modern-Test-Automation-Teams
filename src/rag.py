"""
RAG Pipeline
------------

Handles:
- Semantic retrieval
- Context injection
- Grounded answer generation
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class RAGPipeline:

    def __init__(self, vector_store, llm):

        self.vector_store = vector_store
        self.llm = llm

    # =====================================================
    # MAIN RAG FLOW
    # =====================================================
    def answer(
        self,
        question: str,
        metadata_filter: dict = None
    ):

        logging.info("RAG query received")

        print(f"Metadata filter: {metadata_filter}")

        # ============================================
        # VECTOR SEARCH
        # ============================================
        results = self.vector_store.search(
            query=question,
            top_k=3,
            where=metadata_filter
        )

        print("\nRetrieved docs:", results)

        # ============================================
        # VALIDATE RESULTS
        # ============================================
        if not results:
            return (
                "No relevant QA knowledge found."
            )

        documents = results.get(
            "documents",
            []
        )

        if not documents:
            return (
                "No relevant QA context found."
            )

        if not documents[0]:
            return (
                "No matching QA documents found."
            )

        # ============================================
        # EXTRACT DOCUMENTS
        # ============================================
        retrieved_docs = documents[0]

        # ============================================
        # BUILD CONTEXT
        # ============================================
        context = "\n\n".join(
            retrieved_docs
        )

        # ============================================
        # SAFETY CHECK
        # ============================================
        if not context.strip():

            return (
                "Context retrieval failed."
            )

        # ============================================
        # RAG PROMPT
        # ============================================
        prompt = f"""
You are a Senior QA AI Assistant.

Answer ONLY using the provided QA context.

If the answer is not present in the context,
say:
"Not found in QA knowledge base."

==============================
QA CONTEXT:
==============================

{context}

==============================
USER QUESTION:
==============================

{question}

==============================
ANSWER:
==============================
"""

        # ============================================
        # GENERATE RESPONSE
        # ============================================
        response = self.llm.generate(
            prompt
        )

        return response