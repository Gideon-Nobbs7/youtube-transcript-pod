import requests

response = requests.get("https://api.elevenlabs.io/v1/voices")
print(response.json())
