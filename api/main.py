from fastapi import FastAPI
from pydantic import BaseModel

from src.qa_agent import QAAIAgent

# ============================================
# INITIALIZE FASTAPI
# ============================================
app = FastAPI(
    title="QA AI Agent API",
    description="Offline AI-Powered QA Assistant",
    version="1.0.0"
)

# ============================================
# LOAD QA AGENT
# ============================================
agent = QAAIAgent()

# ============================================
# REQUEST MODEL
# ============================================
class QuestionRequest(BaseModel):
    question: str


# ============================================
# HEALTH CHECK
# ============================================
@app.get("/")
def health_check():

    return {
        "status": "running",
        "service": "QA AI Agent"
    }


# ============================================
# RAG QUESTION API
# ============================================
@app.post("/ask")
def ask_question(request: QuestionRequest):

    response = agent.ask_with_rag(
        request.question
    )

    return response


# ============================================
# MEMORY SEARCH API
# ============================================
@app.post("/search")
def search_memory(request: QuestionRequest):

    response = agent.search_memory(
        request.question
    )

    return response