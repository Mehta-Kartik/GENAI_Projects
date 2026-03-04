## Let's create a simple GENAI App using Langchain
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")
##Prompt Template first of all

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are helpfull assistant please respond to the question"),
        ("user","Question: {question}")
    ]
)

st.write("API:", bool(os.getenv("LANGCHAIN_API_KEY")))
st.write("Trace:", os.getenv("LANGCHAIN_TRACING_V2"))
st.write("Proj:", os.getenv("LANGCHAIN_PROJECT"))  # Must match dashboard

#Streamlit Framework
# st.title("Langchain Demo using  tinyllama:latest")
# input_text=st.chat_input("What is your question")


## Integrating tintllama:latest model
llm=Ollama(model="tinyllama:latest")
output=StrOutputParser()
chain=prompt|llm|output

st.title("Langchain Demo - tinyllama")

# Input at top
input_text = st.text_input("What is your question?", key="user_input")

# Response below input
if input_text:
    with st.spinner("Generating..."):
        response = chain.invoke({"question": input_text})
        st.write(response)