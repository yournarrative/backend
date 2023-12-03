#!/usr/bin/env python
from pprint import pprint
import json
import requests

audio_file_path = "resources/test-audio.mp3"
file = {'file': open(audio_file_path, "rb")}
# data = {"file_type": "m4a"}

# Send to Single Translate
r = requests.post("http://0.0.0.0:5000/api-v1/audioToText/", files=file)
print("Transcribed audio:")
pprint(r.json())

# Get Suggestions
# payload = {"question": "Tell me about yourself?", "answer": r.json()["text"]}
# r = requests.post("http://0.0.0.0:5000/questionAnswerFeedback/", json=payload, headers=headers)
# print("\nSuggestions:")
# pprint(r.json())
