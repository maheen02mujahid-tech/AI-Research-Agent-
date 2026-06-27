# AI Research Agent

AI Research Agent is an AI-powered document intelligence platform that allows users to upload PDF documents, ask natural language questions, generate summaries, and compare concepts using Retrieval-Augmented Generation (RAG).

---

## Features

- Upload and index PDF documents
- Ask questions about uploaded documents using natural language
- Retrieval-Augmented Generation (RAG) with semantic search
- Hybrid RAG with document-grounded responses and general AI knowledge when appropriate
- Conversational memory for follow-up questions
- Automatic document summarization
- Concept comparison
- Source citations with file names, page numbers, and excerpts
- FastAPI backend with interactive Swagger documentation

---

## Tech Stack

### AI & LLM
- OpenAI GPT-4o Mini
- LangChain
- LangGraph
- Retrieval-Augmented Generation (RAG)
- OpenAI Embeddings

### Backend
- Python
- FastAPI
- Pydantic

### Vector Database
- ChromaDB

### Document Processing
- PyPDF
- Recursive Character Text Splitter

---

## Project Architecture

```
User
   │
   ▼
FastAPI REST API
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

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| POST /chat | Ask questions about uploaded documents |
| POST /summarize | Generate a document summary |
| POST /compare | Compare concepts within the documents |
| POST /upload | Upload and index PDF documents |

Interactive API documentation is available at:

```
http://127.0.0.1:8000/docs
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/AI-Research-Agent.git
cd AI-Research-Agent
```

Install dependencies:

```bash
uv sync
```

Create a `.env` file:

```text
OPENAI_API_KEY=your_openai_api_key
```

Run the API:

```bash
python -m uvicorn api:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Example Capabilities

- "What is software redundancy?"
- "Summarize the document."
- "Compare self-checking logic and monotonic logic."
- "Explain it more simply."
- Upload additional PDF documents and query them instantly.

---

## Future Improvements

- Modern web frontend
- User authentication
- Chat history persistence
- Support for additional document formats
- Cloud deployment

---

## Author

**Maheen Mujahid**

Personal project exploring Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), vector databases, LangChain, LangGraph, and FastAPI.