#!/usr/bin/env python
import json
from pprint import pprint
import requests

# audio_file_path = "resources/audio/test-interview.m4a"
# file = {'file': open(audio_file_path, "rb")}
# data = {"info": json.dumps({"question": "Tell me about yourself?"})}

# Send to Single Translate
# r = requests.post("http://0.0.0.0:5001/api-v1/transcribe/audioToSimpleTranscript/", files=file, data=data)
# print("Transcribed audio:")
# # pprint(r.text)
# pprint(r.json())

# Get Suggestions
# payload = {"question": "Tell me about yourself?", "answer": r.json()["text"]}
# r = requests.post("http://0.0.0.0:5001/questionAnswerFeedback/", json=payload, headers=headers)
# print("\nSuggestions:")
# pprint(r.json())


# READ OBJECT FROM S3 AND PROCESS
payload = {"bucket": "ghosted-interviews-test", "key": "f2debf4c-511e-4ac1-879e-6581c0bfeed6/test-interview.m4a"}
r = requests.post("http://0.0.0.0:5001/api-v1/process/audioFileToDatabaseUpdate/", json=payload)
print("Response")
pprint(r.status_code)
