import csv


def write_csv_headers(csv_file):
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Video Title", "Video Link", "Transcript File Path"])


def write_to_csv(video_id, csv_file, video_title, transcript_file_path):
    video_link = f"https://www.youtube.com/watch?v={video_id}"

    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([video_title, video_link, transcript_file_path])
