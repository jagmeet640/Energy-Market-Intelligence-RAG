# Energy Market Intelligence RAG Assistant

A production-style Retrieval-Augmented Generation system for electricity market intelligence.

This project allows users to upload electricity market reports, PDFs, CSV files, and text documents, then ask natural language questions about demand trends, energy prices, market conditions, and forecasting insights.

## Demo Questions

Examples:

- What factors influence electricity demand?
- Why do electricity prices spike?
- How does temperature affect energy usage?
- Summarise the main demand drivers.
- What does the uploaded report say about forecasting?

## Tech Stack

- Python
- FastAPI
- Streamlit
- ChromaDB
- Sentence Transformers
- LangChain text splitters
- Pandas
- Docker

## Architecture

```text
User Uploads Document
        |
        v
Document Loader
        |
        v
Text Chunking
        |
        v
Embedding Model
        |
        v
Chroma Vector Database
        |
        v
Semantic Search
        |
        v
RAG Answer Generation
        |
        v
Streamlit UI / FastAPI Response