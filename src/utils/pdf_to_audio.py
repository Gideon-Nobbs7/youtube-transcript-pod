import os
import urllib.parse

import requests
from dotenv import load_dotenv
from IPython.display import Audio, display

from ..api.routes import logger

load_dotenv()


def parse_to_playai(transcript_url: str):
    api_url = "https://api.play.ai/api/v1/playnotes"

    headers = {
        'AUTHORIZATION': os.getenv("PLAYAI_API_KEY"),
        'X-USER-ID': os.getenv("PLAYAI_USER_ID"),
        'accept': 'application/json'
    }

    files = {
        'sourceFileUrl': (None, transcript_url),
        'synthesisStyle': (None, 'podcast'),
        'voice1': (None, 's3://voice-cloning-zero-shot/baf1ef41-36b6-428c-9bdf-50ba54682bd8/original/manifest.json'),
        'voice1Name': (None, 'Angelo'),
        'voice2': (None, 's3://voice-cloning-zero-shot/e040bd1b-f190-4bdb-83f0-75ef85b18f84/original/manifest.json'),
        'voice2Name': (None, 'Deedee'),
    }

    response1 = requests.post(api_url, headers=headers, files=files)

    if response1.status_code == 201:
        print("Request sent successfully!")
        print(response1.json())
        playNoteId = response1.json().get('id')
        print(f"Generated PlayNote ID: {playNoteId}")

        double_encoooded_id = urllib.parse.quote(playNoteId, safe="")
        final_url = f"{api_url}/{double_encoooded_id}"

        response2 = requests.request("GET", final_url, headers=headers)
        if response2.status_code == 200:
            if response2.json()['status'] == 'completed':
                audio_url = response2.json()['audioUrl']
            elif response2.json()['status'] == 'generating':
                print('Please wait while your PlayNote is being generated and Try again later! ')
            else:
                logger.warning("PlayNote was not successful. Please try again later!")
        else:
            print(response2.text)
        
        wn = Audio(audio_url, autoplay=True)
        return display(wn)
    
    else:
        logger.warning("Failed to generate PlayNote: %s", response1.text)
    
