#!/usr/bin/env python
from pprint import pprint

import requests


headers = {"Content-Type": "application/json"}

# Send to Single Translate
payload = {"audio_bytes": "123"}
r = requests.post("http://0.0.0.0:5000/audioToTextSingle/", json=payload, headers=headers)
print("Transcribed audio:")
pprint(r.json())

# Get Suggestions
payload = {"question": "Tell me about yourself?", "answer": r.json()["text"]}
r = requests.post("http://0.0.0.0:5000/questionAnswerFeedback/", json=payload, headers=headers)
print("\nSuggestions:")
pprint(r.json())
