import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Energy Market RAG Assistant")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./chroma_db")
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)