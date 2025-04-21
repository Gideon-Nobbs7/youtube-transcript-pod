import os
from pathlib import Path

from dotenv import load_dotenv

from .csv_writer import write_csv_headers
from .youtube import get_video_data, get_video_transcript, save_transcript

load_dotenv()


main_dir = Path(__file__).parent.parent.parent
print(main_dir)


def main_utils(youtube_api_key: str, video_link: str):
    if not os.path.exists(f"{main_dir}/transcripts"):
        output_dir = f"{main_dir}/transcripts"
        os.makedirs(output_dir)
    else:
        output_dir = f"{main_dir}/transcripts"

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
        return (video_title, transcript)
        # write_to_csv(video_id, csv_file, video_title, transcript_file_path)


