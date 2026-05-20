"""
QA AI Agent Core Module
-----------------------

Central orchestration layer for:
- Vector search
- RAG retrieval
- Local LLM interaction
- Confidence score calculation
"""

from src.vector_store import VectorStore
from src.ollama_client import OllamaClient
from src.rag import RAGPipeline

from src.prompts import (
    TEST_CASE_PROMPT,
    REVIEW_TEST_CASE_PROMPT,
    BUG_ANALYSIS_PROMPT,
    LOG_ANALYSIS_PROMPT,
    CHECKLIST_PROMPT
)


class QAAIAgent:

    def __init__(self):

        print("Initializing QA AI Agent...")

        # Vector DB
        self.vector_store = VectorStore()

        # Local LLM
        self.llm = OllamaClient()

        # RAG Pipeline
        self.rag = RAGPipeline(
            self.vector_store,
            self.llm
        )

        print("QA AI Agent initialized successfully")

    # =====================================================
    # DIRECT LLM TASKS
    # =====================================================

    def generate_test_cases(self, requirement):

        prompt = TEST_CASE_PROMPT.format(
            input=requirement
        )

        return self.llm.generate(prompt)

    def review_test_cases(self, test_cases):

        prompt = REVIEW_TEST_CASE_PROMPT.format(
            input=test_cases
        )

        return self.llm.generate(prompt)

    def analyze_bug(self, bug_report):

        prompt = BUG_ANALYSIS_PROMPT.format(
            input=bug_report
        )

        return self.llm.generate(prompt)

    def analyze_logs(self, logs):

        prompt = LOG_ANALYSIS_PROMPT.format(
            input=logs
        )

        return self.llm.generate(prompt)

    def create_checklist(self, feature):

        prompt = CHECKLIST_PROMPT.format(
            input=feature
        )

        return self.llm.generate(prompt)

    # =====================================================
    # RAG-BASED QUESTION ANSWERING
    # =====================================================

    def ask_with_rag(self, question):

        """
        RAG flow:
        1. Semantic search
        2. Confidence calculation
        3. Context injection
        4. Grounded answer generation
        """

        try:

            print(f"\nSearching QA memory for: {question}")

            # -------------------------------------------------
            # VECTOR SEARCH
            # -------------------------------------------------
            results = self.vector_store.search(question)

            # -------------------------------------------------
            # VALIDATE RESULTS
            # -------------------------------------------------
            if not results:
                return {
                    "answer": "No relevant QA knowledge found.",
                    "confidence_score": 0
                }

            documents = results.get("documents", [[]])
            distances = results.get("distances", [[]])

            # -------------------------------------------------
            # HANDLE EMPTY SEARCH
            # -------------------------------------------------
            if not documents[0]:
                return {
                    "answer": "No matching QA context found.",
                    "confidence_score": 0
                }

            # -------------------------------------------------
            # BEST MATCH DISTANCE
            # LOWER distance = BETTER match
            # -------------------------------------------------
            best_distance = distances[0][0]

            # -------------------------------------------------
            # CONFIDENCE SCORE CALCULATION
            # -------------------------------------------------
            confidence_score = round(
                max(0, min(100, (1 - best_distance) * 100)),
                2
            )

            print(f"Best semantic distance: {best_distance}")
            print(f"Confidence Score: {confidence_score}%")

            # -------------------------------------------------
            # LOW CONFIDENCE SAFETY
            # -------------------------------------------------
            if confidence_score < 35:
                return {
                    "answer": (
                        "Relevant context not confidently found "
                        "in QA knowledge base."
                    ),
                    "confidence_score": confidence_score
                }

            # -------------------------------------------------
            # GENERATE GROUNDED ANSWER
            # -------------------------------------------------
            answer = self.rag.answer(question)

            # -------------------------------------------------
            # FINAL RESPONSE
            # -------------------------------------------------
            return {
                "answer": answer,
                "confidence_score": confidence_score
            }

        except Exception as e:

            print("RAG Error:", e)

            return {
                "answer": "Error occurred during RAG processing.",
                "confidence_score": 0
            }

    # =====================================================
    # DIRECT VECTOR SEARCH
    # =====================================================

    def search_memory(self, query):

        """
        Direct semantic search without LLM.
        Useful for debugging retrieval quality.
        """

        try:

            results = self.vector_store.search(query)

            return results

        except Exception as e:

            print("Search Error:", e)

            return None