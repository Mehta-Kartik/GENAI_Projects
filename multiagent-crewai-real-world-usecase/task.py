from crewai import Task
from tools import yttools
from agents import blog_resercher,blog_writer

### Research Task
research_task=Task(
    description=(
        "1. Use youtube_channel_search tool with topic='{topic}'\n"
        "2. List top 3 matching Krish Naik videos with URLs\n"
        "3. Describe what each video covers"
    ),  # ✅ FORCE TOOL USE
    expected_output="3 relevant Krish Naik videos with titles, durations, URLs, and summaries",
    agent=blog_resercher,
)

writing=Task(
    description=(
        "get the info from the youtube channel on the topic {topic}"
    ),
    expected_output="Summarize the info from the youtube channel video on the topic {topic} and create the content for the blog",
    tools=[yttools],
    agent=blog_writer,
    async_execution=False,
    output_file="new_blog_post.md",
)

