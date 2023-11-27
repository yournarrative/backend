#!/usr/bin/env python
from pprint import pprint

import requests

payload = {"audio_bytes": "123"}
headers = {"Content-Type": "application/json"}
r = requests.post("http://0.0.0.0:5000/audioToTextSingle/", json=payload, headers=headers)
pprint(f"Transcribed answer: {r.json()}")

# r = requests.get("http://delta-service-alb-prod-2075180613.us-east-2.elb.amazonaws.com/jobData")
pprint(r)
