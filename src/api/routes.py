import logging
import os

from fastapi import HTTPException, status

from ..utils.main import main_utils
from ..utils.txt_to_pdf import generate_pdf_bytes
from .db_config import supabase
from .model import YtPodCreate
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


async def transcript_route(video: YtPodCreate):
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

    pdf_bytes_generated = generate_pdf_bytes(video_transcript)
    pdf_bytes_generated.seek(0)

    try:
        upload_to_bucket = upload_to_store(video_title, pdf_bytes_generated.read())
    except Exception as e:
        logger.warning(f"Error uploading file to supabase bucket: {str(e)}")

    if upload_to_bucket:
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
        print("Response>>>: ", response.data[0])
        return response.data[0]
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error uploading your transcrip, try again later.",
        )
