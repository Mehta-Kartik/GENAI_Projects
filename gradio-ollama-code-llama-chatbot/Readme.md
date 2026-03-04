# Gradio Chatbot using Ollama (CodeLlama)

This repository contains a simple Gradio‑based chat interface that talks to a local LLM running via **Ollama**, using the `/api/generate` endpoint. It wraps a model named `codellama-another` and lets you send prompts and get back generated text.

## What this does
- Connects to a local Ollama server at `http://localhost:11434/api/generate`.
- Uses `requests` to send JSON payloads with:
  - `model` (e.g., `codellama-another`),
  - `prompt` (built from chat history),
  - `stream=False` for a single response.
- Maintains a basic in‑memory conversation history by joining previous prompts.
- Provides a Gradio UI (`gr.Interface`) with a text input and plain text output.

## How to use
1. Install Ollama and pull the model (e.g., `ollama pull codellama` or your custom `codellama-another`).
2. Start the Ollama server (it will listen on `http://localhost:11434` by default).
3. Install dependencies: `gradio`, `requests`.
4. Run `python app.py`.
5. Open the Gradio app in the browser and send prompts to the local CodeLlama model.

## Notes
- This example uses the `/api/generate` endpoint directly; for richer chat behavior, Ollama’s `/api/chat` or its Python client can also be used. [web:105][web:107]  
- The model name (`codellama-another`) must exist in your local Ollama registry; update it if you use a different model.  
