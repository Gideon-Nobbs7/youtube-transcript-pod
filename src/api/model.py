from pydantic import BaseModel, Field


class YtPodCreate(BaseModel):
    video_url: str = Field("A youtue video link")


class YtPodModel(YtPodCreate):
    id: str
    video_title: str
