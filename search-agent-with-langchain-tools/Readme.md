# Search Agent with LangChain Tools & Agents

This repository implements a **search‑enabled AI agent** using LangChain that can answer questions requiring **real‑time web data** by calling search tools (e.g., DuckDuckGo, Tavily, Google Search, etc.). The agent combines LLM reasoning with external search capabilities and optionally maintains conversation memory. [web:167][web:173]

## What this covers
- Creating **tools** (e.g., `DuckDuckGoSearchRun`, `TavilySearchResults`, custom web APIs) that the agent can call. 
- Building an **agent executor** using patterns like `CONVERSATIONAL_REACT_DESCRIPTION`, `TOOL_CALLING`, or LangGraph workflows.  
- Adding **memory** (`ConversationBufferMemory`) so the agent remembers previous searches and context. 
- Handling **dynamic reasoning**: agent decides when to search vs. answer from memory.  

## Tech stack
- Python + LangChain v1 (agents, tools, memory).   
- Search tools: DuckDuckGo, Tavily, Google, Brave Search, etc. 
- LLM backend: OpenAI, Groq, Ollama, or any tool‑calling model.  
- Optional UI: Streamlit, Gradio, or Chainlit for chat interface. 

## How to use
1. Install LangChain and search tool packages (`langchain-community`, `duckduckgo-search`, `tavily-python`).  
2. Set up API keys (Tavily, OpenAI, etc.) via `.env`.  
3. Initialize LLM, tools, and agent executor (e.g., `initialize_agent` or `create_tool_calling_agent`).  
4. Run queries like “What’s the latest news on AI?” and watch the agent search and respond.

This folder serves as a **practical reference** for search‑powered agents from Krish Naik’s GenAI course, perfect for research assistants, news bots, and real‑time Q&A systems.
