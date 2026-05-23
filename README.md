<div align="center"> # 🧪 QA AI Agent

### Offline AI-Powered QA Assistant using RAG, Ollama & ChromaDB

<p align="center">   <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python" />   <img src="https://img.shields.io/badge/Ollama-Local%20LLM-black?style=for-the-badge" />   <img src="https://img.shields.io/badge/ChromaDB-Vector%20DB-green?style=for-the-badge" />   <img src="https://img.shields.io/badge/FastAPI-REST%20API-red?style=for-the-badge&logo=fastapi" />   <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit" />   <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" /> </p> ---

## 🔥 Fully Offline • 100% Private • No API Keys • Open Source

Production-ready QA assistant for QA Engineers and SDETs. Query historical QA knowledge, analyze automation failures, and get grounded AI responses—all running locally.

**No cloud dependencies. No data leakage. Complete control.**

</div> ---

 ---## ✨ What It Does


| Feature                   | Details                                                                                                           |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **RAG-Powered QA**        | Ask questions about your QA knowledge base (bugs, test cases, failures, etc.). Responses grounded in actual data. |
| **REST API**              | FastAPI endpoints for integration with other tools/pipelines                                                      |
| **Interactive Dashboard** | Streamlit UI for real-time queries with confidence scoring                                                        |
| **Flaky Test Analysis**   | Analyzes automation failure logs (Selenium, Playwright) and identifies root causes using AI                       |
| **Offline-First**         | Ollama runs LLMs locally. ChromaDB stores vectors locally. Zero external API calls.                               |
| **Confidence Scoring**    | Every answer includes a confidence score based on semantic similarity to your knowledge base                      |

---

## 📂 Project Structure

```
qa-ai-agent/
├── api.py                    # FastAPI application
├── streamlit_app.py          # Dashboard UI
├── run.py                    # CLI entry point
│
├── src/
│   ├── main.py              # Core CLI logic
│   ├── qa_agent.py          # RAG query engine
│   ├── rag.py               # RAG retrieval pipeline
│   ├── vector_store.py       # ChromaDB vector operations
│   ├── ollama_client.py      # Ollama LLM interface
│   ├── prompts.py           # System prompts
│   └── flaky_analyzer.py    # Flaky test analyzer
│
├── data/
│   └── qa_data/
│       ├── login_bugs/       # Login failure knowledge
│       ├── flaky_tests/      # Flaky test cases & RCAs
│       ├── payment_failures/ # Payment flow issues
│       └── [other domains]   # Add your own QA data
│
├── chroma_db/               # Vector database (persistent)
├── logs/                    # Application logs
├── requirements.txt
└── README.md
```

---

## 🚀 Tech Stack


| Layer            | Technology                           |
| ---------------- | ------------------------------------ |
| **LLM Engine**   | Ollama (LLaMA3 / Mistral)            |
| **Vector DB**    | ChromaDB                             |
| **Embeddings**   | Sentence Transformers                |
| **REST API**     | FastAPI + Swagger                    |
| **Dashboard**    | Streamlit                            |
| **Logging**      | Python Logging + JSON                |
| **Architecture** | RAG (Retrieval-Augmented Generation) |
| **Search**       | Semantic Similarity                  |

---

## 🛠️ Installation

### 1️⃣ Install Ollama

**macOS:**

```bash
brew install ollama
brew services start ollama
```

**Linux/Windows:**[Download from ollama.com](https://ollama.com/)

**Verify installation:**

```bash
ollama --version
```

**Pull a model:**

```bash
ollama pull llama3
# or
ollama pull mistral
```

---

### 2️⃣ Clone Repository & Setup

```bash
git clone https://github.com/SayanCispl/AI-Powered-Offline-QA-Assistant-for-Modern-Test-Automation-Teams.git
cd qa-ai-agent
```

**Create Python virtual environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

**Key dependencies:**

* `fastapi` — REST API framework
* `streamlit` — Dashboard UI
* `chromadb` — Vector database
* `ollama` — LLM client
* `sentence-transformers` — Embeddings

---

### 4️⃣ Load QA Knowledge Base

The system embeds your QA data into ChromaDB on first run:

```bash
python run.py
```

This will:

1. Load QA data from `data/qa_data/` domains
2. Generate embeddings using Sentence Transformers
3. Store vectors in `chroma_db/` (persistent)
4. Start the interactive CLI

---

## 💻 Usage

### Option 1: Interactive CLI

```bash
python run.py
```

You'll get a prompt:

```
Ask your QA question:
> What are common login bugs?

🧠 RAG Answer:
[Grounded response from your knowledge base]

📊 Confidence: 87%
```

---

### Option 2: REST API

Start the FastAPI server:

```bash
fastapi run api.py
# or
python -m uvicorn api:app --reload
```

**API runs on:**`http://127.0.0.1:8000`

**Swagger Docs:**`http://127.0.0.1:8000/docs`

#### Endpoints

**Health Check:**

```bash
curl http://127.0.0.1:8000/
```

**Ask a Question (RAG):**

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are common payment failures?"}'
```

**Search Knowledge Base:**

```bash
curl -X POST http://127.0.0.1:8000/search \
  -H "Content-Type: application/json" \
  -d '{"question": "Selenium timeout issues"}'
```

---

### Option 3: Streamlit Dashboard

Start the interactive dashboard:

```bash
streamlit run streamlit_app.py
```

**Dashboard opens at:**`http://localhost:8501`

Features:

* Text input for QA questions
* Real-time AI responses
* Confidence score visualization
* Progress bar for relevance

---

## 🧠 Core Components

### 1. **QA Agent** (`qa_agent.py`)

The main orchestrator. Handles:

* Vector search against knowledge base
* Prompt building with retrieved context
* LLM response generation
* Confidence score calculation

```python
from src.qa_agent import QAAIAgent

agent = QAAIAgent()
response = agent.ask_with_rag("What causes flaky tests?")
print(response)
```

---

### 2. **RAG Pipeline** (`rag.py`)

Implements Retrieval-Augmented Generation:

1. Convert question to embedding
2. Search ChromaDB for similar QA documents
3. Inject top results into LLM prompt
4. Generate grounded response

**Prevents hallucinations** by ensuring answers come from your actual QA data.

---

### 3. **Vector Store** (`vector_store.py`)

ChromaDB operations:

* Embed documents using Sentence Transformers
* Store vectors with metadata
* Semantic search
* Persistent storage in `chroma_db/`

---

### 4. **Flaky Test Analyzer** (`flaky_analyzer.py`)

Analyzes automation failure logs:

* Parses Selenium/Playwright errors
* Identifies timeout, sync, and DOM issues
* Generates AI-powered RCA
* Recommends fixes based on historical patterns

```python
from src.flaky_analyzer import FlakyTestAnalyzer

analyzer = FlakyTestAnalyzer(llm)
rca = analyzer.analyze(failure_log)
print(rca)
```

---

### 5. **Ollama Client** (`ollama_client.py`)

Interface to local LLM:

* Communicate with Ollama server
* Generate responses using LLaMA3/Mistral
* Handle errors gracefully
* No API keys required

---

## 📊 Confidence Scoring

Every response includes a **confidence score** (0-100):

* **90-100%:** High relevance. Retrieved documents directly match the question.
* **70-89%:** Good relevance. Related QA data found.
* **50-69%:** Low relevance. Limited matching data.
* **Below 50%:** Not found in knowledge base.

Confidence is calculated from **semantic similarity** between the question and retrieved documents.

---

## 🔐 Safety & Hallucination Prevention

The system **only answers using retrieved QA context**. If no relevant data exists:

```
Answer: Not found in knowledge base.
Confidence: 0%
```

This ensures:

* ✅ Reliable, grounded answers
* ✅ Reduced AI hallucinations
* ✅ Enterprise-safe responses
* ✅ Full traceability

---

## 📦 Adding Your Own QA Data

### Step 1: Create a Data Domain

```bash
mkdir -p data/qa_data/your_domain
```

### Step 2: Add QA Documents

Create `.txt` or `.json` files:

```
data/qa_data/your_domain/
├── issue_001.txt
├── issue_002.txt
└── test_case_001.txt
```

Example content:

```
Bug: Login fails on mobile
Root Cause: Session cookie not persisting
Solution: Use localStorage instead of sessionStorage
Tags: login, mobile, cookies
```

### Step 3: Reload Embeddings

```bash
python run.py
```

The system will:

1. Load new documents
2. Generate embeddings
3. Store in ChromaDB
4. Include in future queries

---

## 🧪 Example Queries

Try these questions:

```
What are common login bugs?
Why do flaky tests happen in payment flows?
How do I fix Selenium timeout issues?
What causes DOM synchronization failures?
Generate test cases for authentication
Analyze this error log and find root cause
```

---

## 🚢 Docker Deployment

Build and run in a container:

```bash
docker build -t qa-ai-agent .
docker run -p 8000:8000 -p 8501:8501 qa-ai-agent
```

This starts both the FastAPI server and Streamlit dashboard.

---

## 📋 Requirements

* Python 3.11+
* Ollama (running locally)
* 8GB+ RAM (for LLM + embeddings)
* 2GB+ disk space (for ChromaDB + models)

---

## 🔄 How It Works: Under the Hood

```
User Question
    ↓
[Vector Encoding] → Convert to embedding
    ↓
[ChromaDB Search] → Find similar QA docs
    ↓
[Context Retrieval] → Get top K results
    ↓
[Prompt Building] → Inject context into prompt
    ↓
[Ollama Generation] → LLM generates response
    ↓
[Confidence Calc] → Score based on similarity
    ↓
Grounded Answer + Confidence Score
```

---

## 📝 Logging

Application logs are saved to `logs/`:

```
logs/
├── qa_agent.log
├── api.log
└── analyzer.log
```

Check logs for debugging:

```bash
tail -f logs/qa_agent.log
```

---

## 🤝 Contributing

Found a bug? Want to add features?

Areas to improve:

* Better prompt engineering
* Multi-language support
* Jira/Azure DevOps integration
* Advanced RCA patterns
* Test generation
* CI/CD pipeline integration

---

## 📜 License

MIT License — Free to use, modify, and distribute.

---

## 👨‍💻 Author

**Sayan Koley**
QA Automation Engineer | AI in Testing | Open Source Contributor

---

## ⭐ Support

If this project helped you:

* ⭐ Star the repository
* 🍴 Fork and contribute
* 🐛 Report issues
* 💬 Share feedback

---

## 🔗 Links

* **GitHub:**[Repository](https://github.com/SayanCispl/AI-Powered-Offline-QA-Assistant-for-Modern-Test-Automation-Teams)
* **FastAPI Docs:** Available at `/docs` when API is running
* **Ollama:**[ollama.com](https://ollama.com/)
* **ChromaDB:**[trychroma.com](https://trychroma.com/)

---

<div align="center"> ### 🚀 Ready to Automate QA with AI?

Start with: `python run.py`

</div>
