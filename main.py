import os

from src.youtube import get_video_transcript, get_channel_videos, save_transcript
from src.chatgpt import get_chatgpt_category
from src.csv_writer import write_to_csv, write_csv_headers

from openai import OpenAI


def main(youtube_api_key: str, openai_client: OpenAI, channel_id: str, output_dir: str):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    csv_file = os.path.join(output_dir, "video_details.csv")
    write_csv_headers(csv_file)

    video_data = get_channel_videos(youtube_api_key, channel_id)
    print(f"Found {len(video_data)} videos in the channel.")

    for video_id, video_title in video_data:
        transcript = get_video_transcript(video_id)
        if transcript:
            category = get_chatgpt_category(transcript, openai_api_key)
            if category:
                transcript_file_path = save_transcript(
                    video_id, video_title, transcript, category, output_dir
                )
                write_to_csv(video_id, csv_file)


if __name__ == "__main__":
    # Replace with your YouTube Data API key
    YOUTUBE_API_KEY = ""

    # Replace with your target YouTube channel ID
    CHANNEL_ID = ""

    # Replace with your OpenAI API Key
    OPENAI_API_KEY = ""

    openapi_client = OpenAI(api_key=OPENAI_API_KEY)

    # Directory to save transcripts
    output_dir = "transcripts"

    main(YOUTUBE_API_KEY, openapi_client, CHANNEL_ID, output_dir)
