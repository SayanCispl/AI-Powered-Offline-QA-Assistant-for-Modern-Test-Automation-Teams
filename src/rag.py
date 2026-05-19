class RAGPipeline:
    def __init__(self, vector_store, llm):
        """
        RAG Pipeline Constructor

        Parameters:
        - vector_store : Handles ChromaDB search/retrieval
        - llm          : Handles Ollama LLM generation
        """

        self.vector_store = vector_store
        self.llm = llm

    def answer(self, question: str, metadata_filter: dict = None):
        """
        Main RAG Answer Function

        Flow:
        1. Retrieve relevant QA documents from ChromaDB
        2. Calculate confidence score
        3. Build contextual prompt
        4. Send prompt to LLM
        5. Return formatted AI response
        """

        # ----------------------------------------
        # DEBUG LOGGING
        # ----------------------------------------
        print("Metadata filter:", metadata_filter)

        # ----------------------------------------
        # SEARCH VECTOR DATABASE
        # ----------------------------------------
        # Retrieves top relevant QA documents
        # along with confidence scores
        # ----------------------------------------
        context_docs = self.vector_store.search(
            query=question,
            top_k=3,
            where=metadata_filter
        )

        print("Retrieved docs:", context_docs)

        # ----------------------------------------
        # HANDLE NO RESULTS
        # ----------------------------------------
        if not context_docs:
            return "No relevant QA knowledge found."

        # ----------------------------------------
        # EXTRACT DOCUMENT TEXT
        # ----------------------------------------
        # Convert retrieved document objects
        # into plain context text
        # ----------------------------------------
        context = "\n\n".join(
            [doc["document"] for doc in context_docs]
        )

        # ----------------------------------------
        # CALCULATE AVERAGE CONFIDENCE SCORE
        # ----------------------------------------
        # Confidence is based on vector similarity
        # Higher score = better semantic match
        # ----------------------------------------
        avg_confidence = sum(
            doc["confidence"] for doc in context_docs
        ) / len(context_docs)

        # ----------------------------------------
        # BUILD FINAL PROMPT
        # ----------------------------------------
        prompt = f"""
You are a senior QA expert assistant.

Use ONLY the provided QA knowledge context
to answer the user's question.

If information is missing,
clearly mention limitations.

========================
QA KNOWLEDGE CONTEXT
========================

{context}

========================
USER QUESTION
========================

{question}

========================
ANSWER
========================
"""

        # ----------------------------------------
        # GENERATE RESPONSE FROM LLM
        # ----------------------------------------
        response = self.llm.generate(prompt)

        # ----------------------------------------
        # FINAL FORMATTED OUTPUT
        # ----------------------------------------
        final_response = f"""
Confidence Score: {avg_confidence:.2f}%

RAG Answer:

{response}
"""

        return final_response