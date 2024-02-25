import json
import requests


def send_to_backend(payload, object_key: str):
    backend_url = "GhostedBackendALBProd-2139097039.us-east-1.elb.amazonaws.com"
    api_version = "api-v1"

    if object_key.endswith(".webm"):
        endpoint = "convert/convert/convertAudio"
    else:
        endpoint = "process/audioFileToDatabaseUpdate"

    print(f"Sending request to backend service: url: {backend_url}, "
          f"api_version: {api_version}, endpoint: {endpoint}"
          f"with payload: {payload}")
    try:
        r = requests.post(f"http://{backend_url}/{api_version}/{endpoint}/", json=payload)
        print(f"Response: {r.status_code}")
    except Exception as e:
        print(e)
        print(f"Error processing file {payload['key']} from bucket {payload['bucket']}.")


def lambda_handler(event, context):
    print("Received S3 event: " + json.dumps(event, indent=2))

    for record in event['Records']:

        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        payload = {
            "bucket": bucket,
            "key": key,
            "send_email_when_finished": True,
        }
        send_to_backend(payload)

    print("Processing complete.")
    return
