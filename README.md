# Youtube Transcript Scrapper and Summarizer for Channel Videos

## Step 1: Install Dependencies

Install the required Python libraries using `pip`. Run the following command in your terminal:

```bash
pip install -r requirements.txt
```

## Step 2: Obtain API Keys

### 1. **YouTube Data API Key**

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the **YouTube Data API v3**:
   - Navigate to **APIs & Services** > **Library**.
   - Search for **YouTube Data API v3** and enable it.
4. Create an API key:
   - Go to **APIs & Services** > **Credentials**.
   - Click **Create Credentials** and select **API Key**.
   - Copy the generated API key.

### 2. **OpenAI API Key**

1. Go to the [OpenAI Platform](https://platform.openai.com/).
2. Sign up or log in to your account.
3. Navigate to **API Keys** under your account settings.
4. Click **Create new secret key** and copy the generated API key.

## Step 3: Configure the Script

1. Open the script file (`youtube_transcript_scraper.py`) in a text editor.
2. Replace the following placeholders with your API keys:
   - `YOUTUBE_API_KEY`: Replace with your YouTube Data API key.
   - `OPENAI_API_KEY`: Replace with your OpenAI API key.
3. Replace the `channel_id` variable with the target YouTube channel ID. If you can't find the Channel ID, you can copy the youtube channel link to this website and copy the channel_id from there. [Youtube Channel ID Grabber](https://www.streamweasels.com/%20tools/youtube-channel-id-and-%20user-id-convertor/)

## Step 4: Run the Script

Run the script using the following command in your terminal:

```bash
python -m youtube_transcript_scraper.py
```

## Output

The script will:

1. Fetch all videos from the specified YouTube channel.
2. Download transcripts for each video.
3. Categorize the transcripts using ChatGPT.
4. Save the transcripts in folders named after their categories.
5. Generate a CSV file (`video_details.csv`) containing:
   - Video Title
   - Video Link
   - Transcript File Path

## Folder Structure

After running the script, the output directory (`transcripts/`) will look like this:

```bash
transcripts/
  ├── Music/
  │   ├── dQw4w9WgXcQ_Never_Gonna_Give_You_Up.txt
  ├── Race/
  │   ├── 9bZkp7q19f0_Gangnam_Style.txt
  ├── Technology/
  │   ├── abc123_AI_Revolution.txt
  └── video_details.csv
```

---

## Example CSV Output

The `video_details.csv` file will contain rows like this:

| Video Title               | Video Link                                | Transcript File Path                              |
|---------------------------|-------------------------------------------|--------------------------------------------------|
| Never Gonna Give You Up    | <https://www.youtube.com/watch?v=dQw4w9WgXcQ> | transcripts/Music/dQw4w9WgXcQ_Never_Gonna_Give_You_Up.txt |
| Gangnam Style             | <https://www.youtube.com/watch?v=9bZkp7q19f0> | transcripts/Race/9bZkp7q19f0_Gangnam_Style.txt   |

## Troubleshooting

- **Empty Video List**: Ensure the channel ID is correct and the channel is public.
- **API Key Errors**: Double-check that the API keys are correct and have sufficient quota.
- **Missing Transcripts**: Some videos may not have transcripts available.
