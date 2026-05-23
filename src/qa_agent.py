"""
QA AI Agent Core Module
-----------------------

Central orchestration layer for:
- Vector search
- RAG retrieval
- Local LLM interaction
- Confidence score calculation
- AI flaky test RCA
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

        # =========================================
        # VECTOR DATABASE
        # =========================================
        self.vector_store = VectorStore()

        # =========================================
        # LOCAL LLM
        # =========================================
        self.llm = OllamaClient()

        # =========================================
        # RAG PIPELINE
        # =========================================
        self.rag = RAGPipeline(
            self.vector_store,
            self.llm
        )

        print(
            "QA AI Agent initialized successfully"
        )

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
    # INTERNAL CONFIDENCE CALCULATOR
    # =====================================================

    def _calculate_confidence(
        self,
        distance
    ):

        """
        Convert vector distance
        into confidence score.
        """

        return round(
            max(
                0,
                min(
                    100,
                    (1 - distance) * 100
                )
            ),
            2
        )

    # =====================================================
    # RAG QUESTION ANSWERING
    # =====================================================

    def ask_with_rag(self, question):

        """
        RAG Flow:
        1. Semantic search
        2. Confidence calculation
        3. Context retrieval
        4. Grounded answer generation
        """

        try:

            print(
                f"\nSearching QA memory for: "
                f"{question}"
            )

            # =====================================
            # VECTOR SEARCH
            # =====================================
            results = self.vector_store.search(
                question
            )

            # =====================================
            # HANDLE EMPTY RESULTS
            # =====================================
            if not results:

                return {
                    "answer": (
                        "No relevant QA knowledge found."
                    ),
                    "confidence_score": 0
                }

            documents = results.get(
                "documents",
                [[]]
            )

            distances = results.get(
                "distances",
                [[]]
            )

            # =====================================
            # HANDLE EMPTY DOCS
            # =====================================
            if not documents[0]:

                return {
                    "answer": (
                        "No matching QA context found."
                    ),
                    "confidence_score": 0
                }

            # =====================================
            # BEST MATCH DISTANCE
            # =====================================
            best_distance = distances[0][0]

            confidence_score = (
                self._calculate_confidence(
                    best_distance
                )
            )

            print(
                f"Best semantic distance: "
                f"{best_distance}"
            )

            print(
                f"Confidence Score: "
                f"{confidence_score}%"
            )

            # =====================================
            # LOW CONFIDENCE SAFETY
            # =====================================
            if confidence_score < 35:

                return {
                    "answer": (
                        "Relevant context not confidently "
                        "found in QA knowledge base."
                    ),
                    "confidence_score": confidence_score
                }

            # =====================================
            # GENERATE RAG ANSWER
            # =====================================
            rag_response = self.rag.answer(
                question
            )

            # =====================================
            # HANDLE STRING RESPONSE
            # =====================================
            if isinstance(
                rag_response,
                str
            ):

                return {
                    "answer": rag_response,
                    "confidence_score": confidence_score
                }

            # =====================================
            # HANDLE DICT RESPONSE
            # =====================================
            return {
                "answer": rag_response.get(
                    "answer",
                    "No answer generated."
                ),
                "confidence_score": confidence_score
            }

        except Exception as e:

            print("RAG Error:", e)

            return {
                "answer": (
                    "Error occurred during "
                    "RAG processing."
                ),
                "confidence_score": 0
            }

    # =====================================================
    # AI FLAKY TEST RCA
    # =====================================================

    def analyze_flaky_test(
        self,
        failure_log
    ):

        """
        Analyze flaky automation failures
        using RAG + semantic retrieval.
        """

        enhanced_prompt = f"""
Analyze this flaky automation failure.

Provide:
1. Probable root cause
2. Why the test is flaky
3. Recommended fix
4. Prevention strategy

Automation Failure:
{failure_log}
"""

        return self.ask_with_rag(
            enhanced_prompt
        )

    # =====================================================
    # DIRECT VECTOR SEARCH
    # =====================================================

    def search_memory(self, query):

        """
        Direct semantic search
        without LLM generation.
        """

        try:

            return self.vector_store.search(
                query
            )

        except Exception as e:

            print("Search Error:", e)

            return {
                "documents": [],
                "distances": []
            }