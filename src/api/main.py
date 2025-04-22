import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

# from utils.main import main_utils
from ..utils.main import main_utils
from ..utils.txt_to_pdf import generate_pdf_bytes
from .db_config import supabase
from .model import YtPodCreate, YtPodModel
from .supa_store import get_file_url, upload_to_store

LOG_DIR = "logs"
LOG_FILE = "app.log"

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)


logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler(os.path.join("logs", "app.log"), mode="a", encoding="utf-8")
    ],
)
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


@app.get("/health", summary="Check health service")
async def server_status():
    """
    Simple health check endpoint
    """
    logger.info("Health check endpoint called")
    return {"status": status.HTTP_200_OK}


@app.post(
    "/transcript",
    response_model=YtPodModel,
    status_code=201,
    summary="Get a transcript",
)
async def get_transcript(video: YtPodCreate):
    """ "
    Gets a youtube video's transcript
    """
    video_data = main_utils(
        youtube_api_key=os.getenv("YOUTUBE_API_KEY"), video_link=video.video_url
    )

    if not video_data:
        logger.warning("Youtube video or its transcript could not be found")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video or its transcript could not be found",
        )
    video_title, video_transcript = video_data

    generated_pdf_bytes = generate_pdf_bytes(video_transcript)
    generated_pdf_bytes.seek(0)
    try:
        upload_to_store(video_title, generated_pdf_bytes.read())
    except Exception as e:
        logger.warning(f"Error uploading file to supabase bucket: {str(e)}")

    transcript_url = get_file_url(video_title)

    response = (
        supabase.table("trypod")
        .insert(
            {
                "video_title": video_title,
                "video_url": video.video_url,
                "transcript": transcript_url,
            }
        )
        .execute()
    )
    return response.data[0]


if __name__ == "__main__":
    uvicorn.run(app=app, port=8000, reload=True)
