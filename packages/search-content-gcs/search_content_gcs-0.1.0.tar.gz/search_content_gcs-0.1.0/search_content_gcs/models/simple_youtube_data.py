from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field

class SimpleYouTubeData(BaseModel):
    title: str
    snippet: str
    url: HttpUrl
    video_id: Optional[str] = None
    channel_id: Optional[str] = None
    shorts_id: Optional[str] = None