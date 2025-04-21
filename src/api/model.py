from pydantic import BaseModel, Field


class YtPodModel(BaseModel):
    video_link: str = Field("A youtue video link")
