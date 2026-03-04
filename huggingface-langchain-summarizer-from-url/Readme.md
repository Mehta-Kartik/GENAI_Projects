# Hugging Face + LangChain Summarizer from URL

This repository contains a Streamlit app that summarizes content from **YouTube videos or web pages** using a Hugging Face model via `HuggingFaceEndpoint` and `ChatHuggingFace`, integrated with LangChain components.

## What this does
- Loads content from:
  - YouTube videos (using `YoutubeLoader`).
  - Web pages (using `UnstructuredURLLoader`).
- Passes the extracted text into a LangChain chat‑style pipeline:
  - Prompt template that asks for a **≤300‑word summary**.
  - Model: `Qwen/Qwen2.5-7B-Instruct` on the Hugging Face Hub.
- Displays the generated summary in the Streamlit UI.

## Tech stack
- Python, Streamlit (for UI).
- LangChain v1 style: `ChatPromptTemplate`, `ChatHuggingFace`, `HuggingFaceEndpoint`.
- Web/YouTube loaders: `UnstructuredURLLoader`, `YoutubeLoader`.
- Optional: Groq / Hugging Face credentials via `.env` (HF token here).

## How to use
1. Set your Hugging Face token (or Groq API key, if used) in the sidebar.
2. Enter a YouTube or website URL.
3. Click “Summarize the content from YT or website”.
4. The app will:
   - Load and extract text.
   - Send it through the Hugging Face model via LangChain pipeline.
   - Display the generated summary.
