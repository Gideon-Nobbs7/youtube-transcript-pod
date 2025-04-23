import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

# from utils.main import main_utils
from .model import YtPodCreate, YtPodModel
from .routes import transcript_route

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
    response = transcript_route(video)
    return response


if __name__ == "__main__":
    uvicorn.run(app=app, port=8000, reload=True)
