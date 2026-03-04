from crewai import Agent,LLM
from tools import yttools
# from crewai imoprt 
# #Create a senior blog content 
# llm=LLM(model="groq/llama-3.3-70b-versatile")
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.5,
    max_tokens=1024,
)

blog_resercher=Agent(
    role="Blog Researcher from Youtube Video",
    goal="Get the relevent video content for the topic {topic} from the youtube",
    verbose=True,
    memory=False,
    backstory=(
        "Expert in understanding videos in AI Data Science, Machine Learning and Gen AI and providing suggestion"
    
    ),
    tools=[yttools],
    allow_delegation=False,
    llm=llm,
)

## Creating a senior blog writer agent with yt tool
blog_writer=Agent(
    role="Blog Writer",
    goal="Narrate a compelling tech stories about the video {topic}",
    verbose=True,
    memory=False,
    backstory=(
        "With a flait for simplifying complex topic craft engaging narratives that captivate and educate bringing new discoveries to light in an accessible manner"
    
    ),
    tools=[yttools],
    allow_delegation=False,
    llm=llm,
)