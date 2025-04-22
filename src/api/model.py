from pydantic import BaseModel, Field


class YtPodCreate(BaseModel):
    video_url: str = Field("A youtue video link")


class YtPodModel(YtPodCreate):
    id: str
    created_at: str
    video_title: str
    transcript: str
