import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
# from google import genai
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()
st.write("Jay Ganesh")

##langsmit Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")


#prompt_template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are an perfect time manager. Please assist a student to allocate time to his tasks"),
        ("user","Question:{questions}"),
    ]
)

def generate_response(question,api,model,temperature,max_token):
    # genai.api_key=api
    llm=ChatGoogleGenerativeAI(model=model,google_api_key=api,temperature=temperature,max_output_tokens=max_token)
    # prompt=ChatPromptTemplate()
    parser=StrOutputParser( )
    chat=prompt|llm|parser
    ans=chat.invoke({"questions":question})
    return ans

## Title of the app
st.title("Time Management ChatBot")

st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your API key",type="password")

#dropdown for various model
llm=st.sidebar.selectbox("Select an GEMINI model",["gemini-2.0-flash","gemini-2.5-flash","gemini-2.5-pro"])

temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7,step=0.1)
max_tokens=st.sidebar.slider("Max Tokens",min_value=100,max_value=2048,value=1024,step=64)  


st.write("Go ahead and manage your day")
user_inp=st.text_input("You:")
if user_inp:
    response=generate_response(user_inp,api_key,llm,temperature,max_tokens)
    st.write(response)
else:
    st.write("Please provide the query")