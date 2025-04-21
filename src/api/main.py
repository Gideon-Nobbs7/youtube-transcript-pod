import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

# from utils.main import main_utils
from ..utils.main import main_utils
from .model import YtPodModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()


app = FastAPI(
    title="YtPod",
    description="A FastAPI service that turns a youtube video into a podcast",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.get("/health", summary="Check health service")


async def server_status():
    """
    Simple health check endpoint
    """
    logger.info("Health check endpoint called")
    return {"status": status.HTTP_200_OK}


@app.post("/transcript")
async def get_transcript(video: YtPodModel):
    """ "
    Gets a youtube video's transcript
    """
    video_data = main_utils(
        youtube_api_key=os.getenv("YOUTUBE_API_KEY"), video_link=video.video_link
    )

    if not video_data:
        logger.warning("Youtube video or its transcript could not be found")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video or its transcript could not be found",
        )
    video_title, video_transcript = video_data
    
    return PlainTextResponse(
        content=video_transcript,
        headers={"Content-Disposition": f"attachment; filename={video_title}.txt"},
    )



if __name__ == "__main__":
    uvicorn.run(app=app, port=8000, reload=True)