import os
import re

from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi


def get_channel_videos(api_key, channel_id):
    youtube = build("youtube", "v3", developerKey=api_key)
    video_data = []  # List to store video IDs and titles
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="id,snippet",
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token,
            type="video",
        )
        response = request.execute()

        for item in response["items"]:
            video_id = item["id"]["videoId"]
            video_title = item["snippet"]["title"]
            video_data.append((video_id, video_title))

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return video_data


def get_video_data(api_key, video_link):
    youtube = build("youtube", "v3", developerKey=api_key)
    video_id = video_link.split("=")[1]
    video_data = []

    request = youtube.videos().list(part="id,snippet", id=video_id)
    response = request.execute()

    for item in response["items"]:
        video_id = video_id
        video_title = item["snippet"]["title"]
        sanitized_title = re.sub(r'[\\/*?:"<>|]', "_", video_title)

        video_data.append((video_id, sanitized_title))

    return video_data


def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        transcript_text = " ".join([entry["text"] for entry in transcript])
        return transcript_text

    except Exception as e:
        print(f"Error fetching transcript for video {video_id}: {e}")
        return None


def save_transcript(video_id, video_title, transcript, output_dir):
    if transcript:
        sanitized_title = "".join(
            c if c.isalnum() or c in (" ", "_") else "_" for c in video_title
        )

        filename = os.path.join(output_dir, f"{sanitized_title}.txt")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(transcript)
        print(f"Transcript saved for video {video_id}: {video_title})")
        return filename
    else:
        print(f"There is no transcript for video: {video_title}")
