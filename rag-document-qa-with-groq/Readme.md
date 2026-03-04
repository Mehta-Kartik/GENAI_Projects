# RAG Document Q&A with Groq

This repository contains an end‑to‑end RAG (Retrieval‑Augmented Generation) document Q&A system built with LangChain and Groq’s high‑speed LLM API. It lets you ask questions over your own documents (e.g., PDFs) and get answers grounded in the retrieved context.

## What this covers
- Loading and chunking documents using LangChain text splitters.
- Creating vector embeddings and storing them in a vector database (e.g., FAISS, Chroma, etc.).
- Retrieving relevant document chunks based on user queries.
- Using Groq as the LLM backend to generate answers from the retrieved context.

## Tech stack
- Python, LangChain (v1 style pipelines).
- Groq API (for fast LLM inference).
- Vector store (FAISS / Chroma / similar) and embedding model (e.g., Hugging Face or Google Generative AI).
- Optional: Streamlit or FastAPI for UI/API exposure.

## How to use
1. Set your `GROQ_API_KEY` and other required environment variables.
2. Place your documents (PDFs, text files, etc.) into the designated folder.
3. Run the setup script to load, chunk, and embed documents.
4. Run the RAG Q&A script or app and ask questions to get context‑aware answers.
