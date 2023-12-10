#!/usr/bin/env python
import json
from pprint import pprint
import requests

audio_file_path = "resources/test-interview.m4a"
file = {'file': open(audio_file_path, "rb")}
data = {"info": json.dumps({"question": "Tell me about yourself?"})}

# Send to Single Translate
r = requests.post("http://0.0.0.0:5000/api-v1/audioToTextMultiple/", files=file, data=data)
print("Transcribed audio:")
pprint(r.json())

# Get Suggestions
# payload = {"question": "Tell me about yourself?", "answer": r.json()["text"]}
# r = requests.post("http://0.0.0.0:5000/questionAnswerFeedback/", json=payload, headers=headers)
# print("\nSuggestions:")
# pprint(r.json())
