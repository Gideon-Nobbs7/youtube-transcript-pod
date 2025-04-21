import os

from dotenv import load_dotenv

from src.csv_writer import write_csv_headers, write_to_csv
from src.youtube import get_video_data, get_video_transcript, save_transcript

load_dotenv()


def main(youtube_api_key: str, video_link: str, output_dir: str):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    csv_file = os.path.join(output_dir, "video_details.csv")
    write_csv_headers(csv_file)

    video_data = get_video_data(youtube_api_key, video_link)
    print(f"Found {len(video_data)} videos in the channel.")
    print(video_data)

    for video_id, video_title in video_data:
        transcript = get_video_transcript(video_id)

        transcript_file_path = save_transcript(
            video_id, video_title, transcript, output_dir
        )
        write_to_csv(video_id, csv_file, video_title, transcript_file_path)


if __name__ == "__main__":
    # Replace with your YouTube Data API key
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

    # Replace with your target YouTube channel ID
    VIDEO_LINK = "https://www.youtube.com/watch?v=E2jkAk3PjvM"

    # Directory to save transcripts
    output_dir = "transcripts"

    main(YOUTUBE_API_KEY, VIDEO_LINK, output_dir)
