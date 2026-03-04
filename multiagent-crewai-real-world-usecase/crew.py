from crewai import Crew,Process
# from tools import yttools,
from agents import blog_resercher,blog_writer
from task import research_task,writing

crew=Crew(
    agents=[blog_resercher,blog_writer],
    tasks=[research_task,writing],
    process=Process.sequential,
    memory=False,
    # cache=True,
    max_rpm=100,
    share_crew=True,    
)

#Starting the task execution process with enhanced feedback

result=crew.kickoff(inputs={'topic':"Roadmap for AI/ML"})
print(result)