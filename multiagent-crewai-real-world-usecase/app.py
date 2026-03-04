import streamlit as st
import os
from crewai import Agent, LLM, Crew, Process, Task
from tools import YTChannelTool

st.set_page_config(
    page_title="YouTube → Blog Generator",
    page_icon="🎬",
    layout="wide",  # ✅ Wide layout for blog content
)

st.title("🎬 YouTube Video → Blog Post")
st.markdown("Powered by **CrewAI** + **Groq (Llama 3.3 70B)**")
st.divider()

# ─────────────────────────────────────────
# Sidebar — Configuration (UNCHANGED)
# ─────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")
    
    groq_api_key = st.text_input(
        "🔑 Groq API Key", type="password", placeholder="gsk_..."
    )
    
    st.markdown("---")
    st.markdown("### 🎯 Search Settings")
    
    topic = st.text_input(
        "📌 Topic to Search",
        placeholder="e.g. Data Science Mentorship Program"
    )
    
    channel_url = st.text_input(
        "📺 YouTube Channel URL",
        placeholder="https://www.youtube.com/@krishnaik06/videos",
        value="https://www.youtube.com/@krishnaik06/videos"
    )
    
    model_choice = st.selectbox(
        "🤖 Groq Model",
        ["groq/llama-3.3-70b-versatile", "groq/llama3-8b-8192", "groq/mixtral-8x7b-32768"],
        index=0
    )
    
    st.markdown("---")
    generate_btn = st.button("🚀 Generate Blog Post", use_container_width=True)

# ─────────────────────────────────────────
# Clean Main Area — ONLY Blog Output
# ─────────────────────────────────────────
def run_crew(api_key: str, topic: str, channel_url: str, model: str):
    os.environ["GROQ_API_KEY"] = api_key
    
    yt_tool = YTChannelTool(channel_url=channel_url)
    
    llm = LLM(model=model, temperature=0.5, max_tokens=2048)
    
    researcher = Agent(
        role="Blog Researcher", goal=f"Find relevant videos for '{topic}'",
        verbose=False, memory=False, backstory="YouTube video research expert.",
        tools=[yt_tool], allow_delegation=False, llm=llm
    )
    
    writer = Agent(
        role="Blog Writer", goal=f"Write compelling blog about '{topic}'",
        verbose=False, memory=False, backstory="Engaging tech writer.",
        tools=[yt_tool], allow_delegation=False, llm=llm
    )
    
    research_task = Task(
        description=f"Search YouTube for '{topic}'. List top 3 videos with details.",
        expected_output="3 relevant videos with titles, durations, URLs.",
        agent=researcher, context=[]  # ✅ Explicit context
    )
    
    writing_task = Task(
        description=f"Write detailed blog post on '{topic}' using video research.",
        expected_output="Complete Markdown blog post with intro, sections, conclusion.",
        tools=[yt_tool], agent=writer, 
        context=[research_task],  # ✅ Passes research to writer
        output_file="new_blog_post.md"
    )
    
    crew = Crew(
        agents=[researcher, writer], 
        tasks=[research_task, writing_task],
        process=Process.sequential, 
        memory=False, 
        max_rpm=10,
        verbose=False  # ✅ No logging
    )
    
    result = crew.kickoff(inputs={"topic": topic})
    
    # ✅ EXTRACT THE STRING OUTPUT
    return result.raw if hasattr(result, 'raw') else str(result)

# ─────────────────────────────────────────
# Generation Logic (Clean Center)
# ─────────────────────────────────────────
if generate_btn:
    if not groq_api_key.strip():
        st.error("❌ Enter Groq API Key")
    elif not topic.strip():
        st.error("❌ Enter a topic")
    else:
        with st.spinner(f"🔍 Generating blog for **{topic}**..."):
            try:
                result = run_crew(groq_api_key.strip(), topic.strip(), channel_url.strip(), model_choice)
                
                st.success("✅ Blog generated!")
                st.markdown("---")
                
                # ✅ FULL WIDTH CLEAN BLOG DISPLAY
                st.markdown("# 📝 Generated Blog Post")
                st.markdown(result)
                
                st.download_button(
                    label="⬇️ Download .md", data=result,
                    file_name=f"{topic[:50]}_blog.md", mime="text/markdown",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("**Fixes:** Check API key, rate limits, or YouTube URL")
