# Hybrid Search RAG with Vector Database

This repository implements a **Hybrid Search RAG** pipeline that combines **keyword‑based (sparse)** and **vector‑based (dense)** retrieval to improve the quality of document retrieval for your Retrieval‑Augmented Generation (RAG) system. It uses a vector database (e.g., Pinecone, Chroma, or similar) as the backend store for embeddings.

## What this covers
- Ingest documents and generate embeddings (e.g., text‑embedding models).
- Store embeddings in a vector database and index them for semantic search.
- Combine **BM25 / keyword search** with **vector search** using LangChain’s ensemble retriever or framework‑specific hybrid index.
- Use the merged results as context for an LLM, producing more accurate and robust answers than pure vector or pure keyword search alone. [web:116][web:120]

## Key concepts
- **Hybrid search**: blend of sparse (keyword) and dense (vector) retrieval to get both exact matches and semantically relevant chunks. [web:115][web:119]  
- **Vector database**: FAISS, Pinecone, Chroma, Weaviate, or MongoDB Atlas AI Vector Search used to store and retrieve vector embeddings at scale. [web:118][web:120]  
- **Reranking**: optional step to re‑rank merged results (e.g., via cross‑encoders or MMR) before feeding to the LLM. [web:117][web:120]

## How to use
1. Choose a vector database and set up the index (e.g., Pinecone, Chroma, MongoDB Atlas, etc.).  
2. Load your documents, chunk them, and compute embeddings, then store in the vector store.  
3. Implement a hybrid retriever (e.g., ensemble of BM25 + vector retriever or database‑native hybrid search). [web:116][web:119]  
4. Plug the retriever into a LangChain RAG chain (e.g., `RetrievalQA` or `RetrievalRunnable`) and run queries.

This pattern is especially useful for domain‑specific chatbots, technical Q&A, and any RAG system where you want to balance semantic understanding with precise keyword matching. [web:121][web:124]  
