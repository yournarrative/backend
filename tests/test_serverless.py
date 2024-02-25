import json

from src.serverless import send_s3_file_to_backend


payload = json.load(open("resources/data/s3_event_mp4.json"))
send_s3_file_to_backend.lambda_handler(payload, None)
