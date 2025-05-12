import json
import logging
import os

from fastapi import HTTPException, status

from ..utils.youtube import get_video_data
from ..utils.txt_to_pdf import generate_pdf_bytes
from ..utils.redis import cache
from .db_config import supabase
from .schema import YtPodCreate
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

redis_cache = cache()

async def transcript_route(video: YtPodCreate):
    """ "
    The main route function to the get_transcript endpoint
    Args:
        video: instance of the YtPodCreate model which accepts
               a youutube video's url
    Returns:
        Response model: YtPodModel (id, created_at, video_title, transcript_url)
    """

    video_data = get_video_data(
        api_key=os.getenv("YOUTUBE_API_KEY"), video_link=video.video_url
    )
    print("Video Data:>>>--", video_data)
    if not video_data:
        logger.warning("Youtube video or its transcript could not be found")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video or its transcript could not be found",
        )

    try:
        with generate_pdf_bytes(video_data["video_transcript"]) as pdf_bytes_generated:
            pdf_bytes_generated.seek(0)
            upload_to_store(video_data["video_title"], pdf_bytes_generated.read())
    except Exception as e:
        logger.warning("Error uploading file to supabase bucket: %s", str(e))

    transcript_url = get_file_url(video_data["video_title"])

    response = (
        supabase.table("trypod")
        .insert(
            {
                "name": video.name,
                "video_title": video_data["video_title"],
                "video_url": video.video_url,
                "transcript": transcript_url,
            }
        )
        .execute()
    )
    print("Response>>>: ", response.data[0])
    return response.data[0]



async def get_transcript_route(id: str):
    cached_key = f"video_id:{id}"
    cached_data = redis_cache.get(cached_key)
    if not cached_data:
        response = (
            supabase.table("trypod")
            .select("id", "name", "video_title", "video_url")
            .eq("id", id)
            .execute()
        )

        if not response:
            raise HTTPException(
                status_code=400,
                detail="Try again"
            )

        cached_data = json.dumps(response.data[0])
        redis_cache.setex(cached_key, 15, cached_data)

        return response.data[0]
    
    return json.loads(cached_data)
    