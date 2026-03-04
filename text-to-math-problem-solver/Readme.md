# Text‑to‑Math Problem Solver

This repository implements a **text‑to‑math problem solver** that takes a math question written in natural language (e.g., word problems, arithmetic, algebra, calculus) and returns a step‑by‑step solution backed by an LLM pipeline. It is inspired by the GenAI and LangChain style of projects taught in Krish Naik’s Generative AI course. [web:159][web:162]

## What this does
- Accepts a math question as plain text input (e.g., “What is the derivative of x² + 3x?” or “Solve 2x + 5 = 17”).  
- Uses an LLM agent or chain (with math tools/repl) to parse the problem and compute the answer.   
- Outputs a **step‑by‑step explanation** so students and educators can follow the reasoning.   

## Example patterns
- Basic arithmetic and algebraic expressions.  
- Derivatives, integrals, or simple calculus queries.  
- Formatted results (e.g., boxed final answer) for easy grading or reference.  

## Tech stack
- Python + LLM (e.g., via OpenAI, Groq, Hugging Face, or Ollama).  
- LangChain (optional): agent or `LLMMathChain`‑style setup with a calculator/math tool. 
- Optional UI: Streamlit, Chainlit, or gradio for a simple student‑facing interface.  

## How to use
1. Install dependencies (`langchain`, `numexpr`‑style calculator if used, and your LLM client).  
2. Run the app and type a math question in natural language.  
3. The system will:
   - Parse the question.  
   - Use symbolic or numerical tools + LLM reasoning.  
   - Return a step‑by‑step solution.  

This folder is meant as a **practical reference** for building educational math‑solver agents and math‑oriented RAG/agent systems in Krish Naik’s GenAI course ecosystem. [web:159][web:160]  
