#!/usr/bin/env python
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

payload = {
    "user_email": "shayaan.jagtap@gmail.com",
    "content": "I am working on two projects - one interview analyzer that converts "
               "interviews into actionable feedback, and another project that stores and retrieves "
               "information about all about a persons career",
    "question": "What projects are you working on?",
    "document_type": "Q&A"

}
r = requests.post("http://0.0.0.0:5001/api-v1/insert/insertDocument/", json=payload)

print("Uploaded document for shayaan.jagtap@gmail.com")
pprint(r.status_code)

payload = {
    "user_email": "tryghosted@gmail.com",
    "content": "I am working on a project that converts blackholes to unlimited energy sources",
    "question": "What projects are you working on?",
    "document_type": "Q&A"
}
r = requests.post("http://0.0.0.0:5001/api-v1/insert/insertDocument/", json=payload)

print("Uploaded document for tryghosted@gmail.com")
pprint(r.status_code)


payload = {
    "user_email": "shayaan.jagtap@gmail.com",
    "query": "What skills have I learned and what projects have I worked on?"
}
r = requests.post("http://0.0.0.0:5001/api-v1/query/queryUserHistory/", json=payload)

print("Response for query shayaan.jagtap@gmail.com")
pprint(r.status_code)
pprint(r.text)

payload = {
    "user_email": "tryghosted@gmail.com",
    "query": "What skills have I learned and what projects have I worked on?"
}
r = requests.post("http://0.0.0.0:5001/api-v1/query/queryUserHistory/", json=payload)

print("Response for query tryghosted@gmail.com")
pprint(r.status_code)
pprint(r.text)
