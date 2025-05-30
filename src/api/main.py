import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache

from ..utils.pdf_to_audio import parse_to_playai
from .schema import YtPodCreate, YtPodModel, YtPodOut
from .routes import transcript_route, get_transcript_route

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
    summary="Generate a transcript",
)
async def generate_transcript(video: YtPodCreate):
    """ "
    Gets a youtube video's transcript and generate a podcast audio

    Args:
        video: instance of the YTPodCreate model
    Returns:
        A parsed output from PlayAI in an audio form
    """
    response = await transcript_route(video)
    transcript_url = response["transcript"]
    # parse_response = parse_to_playai(transcript_url)
    return response


@app.get(
    "/get-transcript/{id}",
    response_model=YtPodOut,
    status_code=200,
    summary="Get the transcript data"
)
async def get_transcript_from_db(id: str):
    response = await get_transcript_route(id)
    return response


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
