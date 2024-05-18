#!/usr/bin/env python

from pprint import pprint
import requests


def print_response(r, test: str, print_json=False):
    print(f"Response for test {test}:")
    pprint(r.status_code)
    if print_json:
        pprint(r.json())

    print('\n')


def create_activities_for_user():
    activities = [
        {
            "title": "Test Activity for User 2",
            "description": "Building a Python API Server using FastAPI and Docker to get Narrative launched",
            "category": "Skill",
            "status": "Completed",
        },
        {
            "title": "Test Second Activity for User 2",
            "description": "Helping get the designs, tech, and copy ready to launch Narrative",
            "category": "Achievement",
            "status": "In Progress",
        },
    ]
    data = {"user_id": "3cc8c13d-d731-4bd0-a6e1-e3e214ad7c7e", "activities": activities}

    r = requests.post("http://0.0.0.0:5001/api-v1/activities/insertActivities/", json=data)
    print_response(r, "create_activities_for_user")


def create_brag_doc(user_id):
    data = {
        "user_id": user_id,
        "publish": True,
        "url": "shayaanjagtap2",
    }

    r = requests.post("http://0.0.0.0:5001/api-v1/brag-doc/updateBragDoc/", json=data)
    print_response(r, "create_brag_doc")


def get_brag_doc_for_user(user_id):
    r = requests.get(f"http://0.0.0.0:5001/api-v1/brag-doc/getBragDocForUser/{user_id}")
    print_response(r, "get_brag_doc_for_user")


def run_tests():
    user_id = "b945a7c8-171f-454f-b6f8-e42d778fd889"
    # create_activities_for_user()
    create_brag_doc(user_id)
    # get_brag_doc_for_user(user_id)


if __name__ == '__main__':
    run_tests()
