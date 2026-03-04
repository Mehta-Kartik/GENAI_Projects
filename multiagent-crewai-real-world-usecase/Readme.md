# Multi‑Agent System Using CrewAI for Real‑World Use Case

This repository implements a **multi‑agent workflow built with CrewAI**, as part of the *Complete Generative AI Course with LangChain and Huggingface* by Krish Naik. It focuses on a **real‑world use case**, such as a research‑to‑report pipeline, customer‑support assistant, or content‑generation crew, where multiple specialized agents collaborate to solve a complex task end‑to‑end.

## What this covers
- Designing **roles and agents** (e.g., Researcher, Writer, Reviewer, QA) with clear goals and backstories.  
- Defining **tasks** and connecting them into a crew so agents hand off work automatically
- Using **tools** (web search, file I/O, APIs, RAG, etc.) to make the agents operate on real data.  

## Example real‑world pattern
- A user asks a question (e.g., “Create a market research report on X”).
- A **Researcher agent** gathers information from the web or internal docs.
- A **Writer agent** composes a structured report from the collected data.
- A **Reviewer agent** checks tone, facts, and formatting.  
- The final output is returned as a polished document or knowledge artifact.

## Tech stack
- Python + **CrewAI** framework.
- LLM backend (e.g., OpenAI, Groq, Hugging Face, or Ollama).  
- Optional: RAG layer, vector DB, or external tools (search, email, Notion, Slack, etc.).

## How to use
1. Install `crewai` and your chosen LLM integration.  
2. Define agents and tasks (in code or YAML) for your target use case. 
3. Create a `Crew` object that chains the agents and start execution with `crew.kickoff()`.  
4. Inspect logs and outputs; then extend the agents for your own domain (marketing, customer support, technical docs, etc.).  

This folder is meant as a **practical, production‑like reference** for multi‑agent CrewAI patterns from Krish Naik’s GenAI course.
