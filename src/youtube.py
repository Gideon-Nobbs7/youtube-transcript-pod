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


def get_video_transcript(video_id):
    languages = ["en"]
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        try:
            transcript = transcript_list.find_manually_created_transcript(languages)
        except:  # noqa: E722
            transcript = transcript_list.find_generated_transcript(languages)

        transcript_text = " ".join([entry["text"] for entry in transcript])
        return transcript_text

    except Exception as e:
        print(f"Error fetching transcript for video {video_id}: {e}")
        return None


def save_transcript(video_id, video_title, transcript, category, output_dir):
    sanitized_title = "".join(
        c if c.isalnum() or c in (" ", "_") else "_" for c in video_title
    )
    sanitized_category = "".join(
        c if c.isalnum() or c in (" ", "_") else "_" for c in category
    )

    category_folder = os.path.join(output_dir, sanitized_category)
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)

    filename = os.path.join(category_folder, f"{video_id}_{sanitized_title}.txt")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(transcript)
    print(
        f"Transcript saved for video {video_id}: {video_title} (Category: {category})"
    )

    return filename
