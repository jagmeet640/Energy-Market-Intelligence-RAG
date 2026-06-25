import os
import shutil
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.rag_pipeline import RAGPipeline
from app.config import APP_NAME

app = FastAPI(title=APP_NAME)

rag = RAGPipeline()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Energy Market RAG Assistant is running."
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs("data/raw", exist_ok=True)

    file_path = f"data/raw/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = rag.ingest_file(
        file_path=file_path,
        source_name=file.filename
    )

    return result


@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = rag.answer_question(request.question)
    return result