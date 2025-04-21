import openai
from openai import OpenAI


def get_chatgpt_category(transcript: str, client: OpenAI):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that categorizes YouTube video transcripts into a single-word theme. Examples include Morality, Race, Technology, etc.",
                },
                {
                    "role": "user",
                    "content": f"Based on the following transcript, provide a single-word category that best describes its theme:\n\n{transcript}",
                },
            ],
            max_tokens=10,
            temperature=0.5,
        )
        category = response["choices"][0]["message"]["content"].strip()
        return category
    except Exception as e:
        print(f"Error getting category from ChatGPT: {e}")
        return None
