# schemas.py

from pydantic import BaseModel
from datetime import datetime

class VideoProfileSchema(BaseModel):
    id: int
    video_id: str
    title: str
    channel_title: str
    publish_time: datetime
    views: int
    likes: int
    dislikes: int
    like_ratio: float
    category_name: str
    days_till_viral: int

    class Config:
        orm_mode = True
