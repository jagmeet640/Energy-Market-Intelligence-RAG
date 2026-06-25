import chromadb
from sentence_transformers import SentenceTransformer
from app.config import VECTOR_DB_PATH, EMBEDDING_MODEL


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection(
            name="energy_market_docs"
        )
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    def add_documents(self, chunks: list[str], source_name: str):
        embeddings = self.embedding_model.encode(chunks).tolist()

        ids = [f"{source_name}_{i}" for i in range(len(chunks))]

        metadata = [
            {"source": source_name, "chunk_id": i}
            for i in range(len(chunks))
        ]

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadata
        )

    def search(self, query: str, top_k: int = 5):
        query_embedding = self.embedding_model.encode([query]).tolist()[0]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results