import validators
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
# from langchain_community.document_loaders.youtube import YTTranscriptLoader  # Fixed YT loader
from langchain_community.document_loaders import YoutubeLoader  # ✅ Correct
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
import os
from dotenv import load_dotenv
load_dotenv()
# Streamlit App
st.set_page_config(page_title="Langchain: Summarize Text from YT or Website")
st.title("Langchain: Summarize Text from YT or Website")
st.subheader('Summarize URL')

# Get the Groq Api key
with st.sidebar:
    api_key = st.text_input("HF Token Key", value="", type="password")

if api_key.strip():
    # llm = ChatGroq(groq_api_key=api_key, model="openai/gpt-oss-20b")
    repo_id = "Qwen/Qwen2.5-7B-Instruct"

    llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        max_new_tokens=512,
        temperature=0.8,
        huggingfacehub_api_token=api_key,
        task="conversational"   # explicitly match the model's registered task
    )

    chat_model=ChatHuggingFace(llm=llm)
    
    prompt = ChatPromptTemplate.from_template("""
    Provide a summary of the following content in 300 words or less.
    
    Content: {text}
    
    Summary:
    """)

    url = st.text_input('Enter Youtube URL or Webpage URL', label_visibility="collapsed")

    if st.button("Summarize the content from YT or website"):
        # Validate all the inputs
        if not url.strip():
            st.error("Please provide a valid URL")
        elif not validators.url(url):
            st.error("Please enter a valid URL")
        else:
            try:
                with st.spinner("Analyzing content..."):
                    # Loading the web and URL data
                    if "youtube.com" in url or "youtu.be" in url:
                        loader = YoutubeLoader.from_youtube_url(url, language="en")  # Add add_video_info=True if needed
                    else:
                        loader = UnstructuredURLLoader(
                            urls=[url],
                            ssl_verify=False,
                            headers={
                                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
                            }
                        )
                    
                    data = loader.load()
                    
                    # Join content for summarization
                    text = "\n\n".join([doc.page_content for doc in data])
                    
                    # Chain for summarization task
                    chain = prompt | chat_model # Simpler pipe chain
                    output_summary = chain.invoke({"text": text})
                    
                    st.success("**Summary:**")
                    st.write(output_summary.content)
                    
            except Exception as e:
                st.error(f"Error processing URL: {str(e)}")
                st.info("Tips: Use public YouTube videos with transcripts. Try a different URL if issues persist.")
else:
    st.info("👈 Please add your Groq API key in the sidebar to get started!")
