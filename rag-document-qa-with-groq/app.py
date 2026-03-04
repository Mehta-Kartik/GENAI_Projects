import streamlit as st
import os

# ✅ LLMs
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

# ✅ Text Splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ✅ Modern v1.x RAG Components
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ✅ Vector store & PDF Loader
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

# ✅ File upload helper
from langchain_text_splitters import CharacterTextSplitter


#Embeddings
from langchain_community.embeddings import OllamaEmbeddings
# from langchain_google_genai import 



from dotenv import load_dotenv
load_dotenv()

os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
groq_api=os.getenv("GROQ_API_KEY")
llm=ChatGroq(groq_api_key=groq_api,model_name="openai/gpt-oss-20b")

prompt=ChatPromptTemplate.from_template(
    """
    Answer The questions based on the provided context memory
    Please provide the most accurate response based on the question
    <context>
    {context}
    </context>
    Question:{question}
    """
)


def create_embedding_vectors():
    # ✅ Folder check
    if not os.path.exists("./researchPaper"):
        st.error("❌ ./researchPaper missing!")
        return
        
    loader = PyPDFDirectoryLoader("./researchPaper", glob="**/*.pdf")  # Explicit PDF filter
    st.info(f"🔍 Scanning ./researchPaper...") 
    
    try:
        docs = loader.load()
        st.success(f"✅ Loaded {len(docs)} PDFs successfully!")
        st.session_state.documents = docs
    except Exception as e:
        st.error(f"❌ PDF loading failed: {str(e)}")
        st.session_state.documents = []
        return

    if not st.session_state.documents:
        st.error("❌ 0 PDFs loaded. Check file formats.")
        # List files for debug
        files = os.listdir("./researchPaper")
        st.write("Files found:", files)
        return

    # List first doc metadata
    st.write("📄 Sample doc:", st.session_state.documents[0].metadata)
    
    # Rest unchanged...
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    st.session_state.finaldoc = text_splitter.split_documents(st.session_state.documents)
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    st.session_state.vectors = FAISS.from_documents(st.session_state.finaldoc, embeddings)
    st.success(f"✅ Vector store ready: {len(st.session_state.finaldoc)} chunks!")


usr_prompt=st.text_input("Input your questions:")
if st.button("Document Embeddings"):
    create_embedding_vectors()
    st.write("Vector Embeddings are ready")
import time 
if usr_prompt and st.session_state.get("vectors") is not None:
    retriever = st.session_state.vectors.as_retriever(search_kwargs={"k": 3})
    
    # ✅ FIXED CHAIN - extract .content
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt 
        | llm 
        | StrOutputParser()  # ← Converts AIMessage → string
    )
    
    start = time.time()
    response = chain.invoke(usr_prompt)
    st.markdown(response)  # Clean formatting
    
    # ✅ Get sources SEPARATELY (not from response)
    docs = retriever.invoke(usr_prompt)
    st.info(f"⏱️ Response time: {time.time()-start:.2f}s")
    
    with st.expander(f"📚 Sources ({len(docs)} docs found)"):
        for i, doc in enumerate(docs):
            with st.container():
                st.write(f"**Doc {i+1}:**")
                st.write(doc.page_content[:400] + "..." if len(doc.page_content) > 400 else doc.page_content)
                st.caption(f"Page {doc.metadata.get('page', 'N/A')}, Source: {doc.metadata.get('source', 'Unknown')}")
                st.divider()
