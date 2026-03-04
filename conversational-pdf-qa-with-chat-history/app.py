##RAG QNA including chat history

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import os
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
load_dotenv()

os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")

embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

st.title("Conversation QNA with chat history")
st.write("Upload PDF file and chat with their content")

api_key=st.text_input("Enter your GROQ API KEY",type="password")

if api_key:
    model=ChatGroq(groq_api_key=api_key,model_name="openai/gpt-oss-20b")

    #Chat Interface
    session_id=st.text_input("Session Id",value="default_session")

    #storing the session id and its conversation

    if 'store' not in st.session_state:
        st.session_state.store={}
    
    uploaded_file=st.file_uploader("Upload a PDF file",type="pdf",accept_multiple_files=False)
    
    if uploaded_file:
        documents=[]
        # for uploaded_file in uploaded_file:
        temppdf=f"./temp.pdf"
        with open(temppdf,'wb') as f:
            f.write(uploaded_file.getvalue())
            # f.name=uploaded_file.name
        loader=PyPDFLoader(temppdf)
        docs=loader.load()
        documents.extend(docs)
        ##Spliting and creating embeddings for the documents
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=5000,chunk_overlap=300)
        splits=text_splitter.split_documents(documents)
        vectorstoredb=Chroma.from_documents(documents=splits,embedding=embeddings)
        retriever=vectorstoredb.as_retriever()
    
    contextualize=(
        "Given  a chat history and the latest user question which might reference context in the chat history formulate a standalone question which can be understood without the chat history.Do NOT answer the question just reformulate it if needed and otherwise return as it is."
    )
    
    contextualize_q_prompt=ChatPromptTemplate.from_messages(
        [
            ("system",contextualize),
            MessagesPlaceholder("chat_history"),
            ("human",'{input}')
        ]
    )
    chathistoryawareretriever = (
        contextualize_q_prompt       # Gets full dict: {input, chat_history}
        | model
        | StrOutputParser()           # → standalone question string
        | retriever                   # → docs
    )

    #Answer question
    system_prompt = (
        "You are an assistant for question answering tasks. "
        "Use the following retrieved context to answer the question. "
        "If you don't know the answer, say that you don't know. "
        "Use three sentences maximum and keep the answer concise.\n\n"
        "{context}\n\n"

    )

    qa_prompt= ChatPromptTemplate.from_messages(
        [
            ("system",system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human","{input}")
        ]
    )

    qa_chain=qa_prompt| model
    # Keep chathistoryawaretreiver and qa_prompt as-is

    rag_chain = (
        RunnablePassthrough.assign(
            context=chathistoryawareretriever  # Adds context, keeps input + chat_history
        )
        | qa_prompt
        | model
        | StrOutputParser()
    )

    def get_session_history(session:str)->BaseChatMessageHistory:
        if session not in st.session_state.store:
            st.session_state.store[session]=ChatMessageHistory()
        return st.session_state.store[session]
    
    conversation_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"  # Match if your prompt outputs to this
    )
    user_inp=st.text_input("Your question: ")
    if user_inp:
        session_history=get_session_history(session_id)
        response=conversation_rag_chain.invoke(
            {"input":user_inp},
            config={
                "configurable":{"session_id":session_id}
            },
        )
        st.write(st.session_state.store)
        st.success("Assistant:"+response)
        st.write("Chat History",session_history.messages)
else:
    st.warning("Please enter the groq api key")