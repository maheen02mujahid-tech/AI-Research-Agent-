from pathlib import Path
import shutil

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from src.document_loader import load_and_split_pdf
from src.vector_store import load_vector_store, add_documents_to_vector_store
from src.assistant import AIResearchAssistant
from src.agent import build_research_agent

load_dotenv()

app = FastAPI(title="AI Research Agent")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_store = load_vector_store()
assistant = AIResearchAssistant(vector_store)
agent = build_research_agent(assistant)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def home():
    return {"message": "AI Research Agent API is running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = agent.invoke({
        "user_input": request.message
    })

    return ChatResponse(answer=result["answer"])


@app.post("/summarize", response_model=ChatResponse)
def summarize():
    summary = assistant.summarize()
    return ChatResponse(answer=summary)


@app.post("/compare", response_model=ChatResponse)
def compare(request: ChatRequest):
    comparison = assistant.compare(request.message)
    return ChatResponse(answer=comparison)


@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    data_folder = Path("data")
    data_folder.mkdir(exist_ok=True)

    file_path = data_folder / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = load_and_split_pdf(str(file_path))
    add_documents_to_vector_store(chunks)

    return {
        "message": "PDF uploaded and indexed successfully",
        "filename": file.filename,
        "chunks_created": len(chunks)
    }