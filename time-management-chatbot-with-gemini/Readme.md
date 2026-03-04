# Time Management Chatbot with Gemini and LangChain

This repository contains a Streamlit‑based chatbot that helps students manage their time by planning and allocating time slots to tasks. The chatbot uses Google’s Gemini models via `langchain_google_genai` and follows the LangChain v1 pattern with `ChatPromptTemplate | ChatGoogleGenerativeAI | StrOutputParser`.

## Features
- Simple UI built with Streamlit (title, sidebar, sliders for temperature and max tokens, model selection).
- Integration with Gemini (`gemini-2.0-flash`, `gemini-2.5-flash`, `gemini-2.5-pro`) through LangChain.
- Prompt template that instructs the LLM to act as a “perfect time manager”.
- LangChain tracing enabled via environment variables (`LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT`).

## How to run
1. Set your `GOOGLE_API_KEY` and `LANGCHAIN_API_KEY` in a `.env` file.
2. Install required packages: `streamlit`, `langchain-google-genai`, `langchain-core`, `python-dotenv`.
3. Run: `streamlit run app.py` (or whatever file name you use).
