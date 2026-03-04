import yt_dlp
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class SearchInput(BaseModel):
    topic: str = Field(..., description="Topic to search Krish Naik channel")

class YTChannelTool(BaseTool):
    name: str = "youtube_channel_search"
    description: str = "Searches ANY YouTube channel for relevant videos by topic."
    args_schema: Type[BaseModel] = SearchInput
    channel_url: str = Field(  # ✅ Pydantic Field — this fixes the error!
        default="https://www.youtube.com/@krishnaik06/videos",
        description="YouTube channel videos URL"
    )
    
    def _run(self, topic: str) -> str:
        # Your existing code stays EXACTLY the same!
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'playlistend': 50,
            'ignoreerrors': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(self.channel_url, download=False)
                entries = info.get('entries', []) or []
                print(f"Found {len(entries)} videos")
            except Exception as e:
                return f"❌ YouTube fetch failed: {str(e)}"
        
        # ... rest of your matching logic stays the same
        keywords = topic.lower().split()
        synonyms = {
            'ai': ['ai', 'artificial intelligence', 'genai', 'generative ai'],
            'ml': ['ml', 'machine learning'],
            'dl': ['dl', 'deep learning'],
            'data': ['data science', 'datascience', 'data'],
            'science': ['data science', 'datascience']
        }
        
        relevant_videos = []
        for i, entry in enumerate(entries[:30]):
            if not entry or not entry.get('title'):
                continue
                
            title_lower = entry.get('title', '').lower()
            match = False
            for kw in keywords:
                syns = synonyms.get(kw, [kw])
                if any(syn in title_lower for syn in syns):
                    match = True
                    break
            
            if match:
                duration = entry.get('duration', 'N/A')
                vid_id = entry.get('id', 'N/A')
                relevant_videos.append(
                    f"**{entry['title']}**\n"
                    f"⏱️ Duration: {duration}s\n"
                    f"🔗 https://youtube.com/watch?v={vid_id}\n"
                    f"---"
                )
        
        if relevant_videos:
            return "\n".join(relevant_videos[:5])
        else:
            return f"❌ No matches for '{topic}'. Found {len(entries)} total videos."

# ✅ Now both work perfectly:
yttools = YTChannelTool()  # Default Krish Naik
custom_tool = YTChannelTool(channel_url="https://www.youtube.com/@codebasics/videos")  # Custom
