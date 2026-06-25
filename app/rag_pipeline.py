from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.document_loader import load_document
from app.vector_store import VectorStore


class RAGPipeline:
    def __init__(self):
        self.vector_store = VectorStore()

    def chunk_text(self, text: str) -> list[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=120
        )
        return splitter.split_text(text)

    def ingest_file(self, file_path: str, source_name: str):
        text = load_document(file_path)
        chunks = self.chunk_text(text)
        self.vector_store.add_documents(chunks, source_name)

        return {
            "source": source_name,
            "chunks_created": len(chunks),
            "status": "success"
        }

    def answer_question(self, question: str):
        results = self.vector_store.search(question, top_k=5)

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        context = "\n\n".join(documents)

        answer = self.generate_answer(question, context)

        return {
            "question": question,
            "answer": answer,
            "sources": metadatas,
            "retrieved_context": documents
        }

    def generate_answer(self, question: str, context: str) -> str:
        """
        Simple local response generator.
        You can later replace this with OpenAI, Gemini, Claude, or Groq.
        """

        if not context.strip():
            return "I could not find enough relevant information in the uploaded documents."

        return f"""
Based on the retrieved electricity market documents, here is the answer:

Question:
{question}

Relevant Evidence:
{context[:2000]}

Summary:
The available context suggests that the answer should be based on the retrieved market data and documents above. 
For a production deployment, this function can be connected to an LLM to generate a polished final response.
"""