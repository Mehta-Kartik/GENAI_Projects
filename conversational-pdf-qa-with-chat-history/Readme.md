# Conversational Q&A Chatbot with PDFs and Chat History

This repository contains a conversational RAG (Retrieval‑Augmented Generation) chatbot that lets you **chat with PDF documents** while maintaining **full chat history** across turns. It is designed as a follow‑along implementation from the *Complete Generative AI Course with LangChain and Huggingface* by Krish Naik, enhanced with memory and document handling.

## What this covers
- Upload and process PDFs (text extraction + chunking).
- Create embeddings and store them in a vector store (e.g., FAISS/Chroma).
- Retrieve relevant document chunks for each question.
- Use an LLM (e.g., via Groq or another provider) to answer questions grounded in the PDF + past conversation.
- Track and re‑inject chat history so follow‑up questions are context‑aware.

## Key features
- PDF‑based Q&A: ask questions about the content of uploaded PDFs.
- Conversational flow: bot remembers previous questions and answers.
- RAG pipeline: retrieval from vector store + generation from LLM.
- Optional UI: Streamlit or FastAPI can be wired on top for a nicer front‑end.

## How to use
1. Set required environment variables (e.g., API keys, embedding model config).
2. Run the setup script to load and index your PDFs into the vector store.
3. Launch the chat app and upload PDFs.
4. Ask questions; the bot will answer using document content and conversation history.
