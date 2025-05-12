from pydantic import BaseModel, Field


class YtPodCreate(BaseModel):
    name: str = Field("A custom name for your yt-pod")
    video_url: str = Field("A youtue video link")


class YtPodModel(YtPodCreate):
    id: str
    created_at: str
    video_title: str
    transcript: str


class YtPodOut(BaseModel):
    id: str
    name: str
    video_title: str
    video_url: str