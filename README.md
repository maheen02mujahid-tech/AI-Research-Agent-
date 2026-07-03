# AI Research Agent

An AI-powered document intelligence platform. Upload a PDF, ask questions, get answers with source citations.

**[Live Demo](https://maheen02mujahid-tech.github.io/AI-Research-Agent-)** — 3 free questions per visitor

---

## What It Does

- Upload and index PDF documents
- Ask natural language questions about your documents
- Get answers with source citations including file name and page number
- Summarize documents automatically
- Compare concepts across documents
- Conversational memory for follow-up questions

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | OpenAI GPT-4o Mini |
| RAG Pipeline | LangChain, LangGraph |
| Vector Database | ChromaDB |
| Embeddings | OpenAI Embeddings |
| Backend | Python, FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render (backend), GitHub Pages (frontend) |

---

## Architecture

```
User
   │
   ▼
GitHub Pages (Frontend)
   │
   ▼
FastAPI REST API (Render)
   │
   ▼
LangGraph Agent
   │
   ├── Question Answering
   ├── Document Summarization
   └── Concept Comparison
   │
   ▼
LangChain Retrieval
   │
   ▼
ChromaDB Vector Store
   │
   ▼
OpenAI Embeddings
```

---

## Try the Demo

A sample document is included in the `data/` folder (`ArtificialIntellegence.pdf`). Upload it and try:

- "What is Artificial Intelligence?"
- "Who invented AI and when?"
- "What are the pros and cons of AI?"
- "What is a Support Vector Machine?"
- "What are some real-world applications of AI?"

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload and index a PDF |
| `POST` | `/chat` | Ask a question |
| `POST` | `/summarize` | Summarize documents |
| `POST` | `/compare` | Compare concepts |

Interactive API docs: `http://127.0.0.1:8000/docs`

---

## Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/maheen02mujahid-tech/AI-Research-Agent-.git
cd AI-Research-Agent-
```

**2. Create a virtual environment**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Create a `.env` file**

```
OPENAI_API_KEY=your_openai_api_key_here
```

**5. Start the backend**

```bash
python -m uvicorn api:app --reload
```

**6. Open the frontend**

```bash
cd frontend
python -m http.server 5500
```

Then visit `http://localhost:5500`

---

## Author

**Maheen Mujahid**

Built to explore LLMs, Retrieval-Augmented Generation, vector databases, LangChain, LangGraph, and FastAPI.