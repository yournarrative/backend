#!/usr/bin/env python

from pprint import pprint

import requests


def print_response(r, test: str, print_json=False):
    print(f"Response for test {test}:")
    pprint(r.status_code)
    if print_json:
        pprint(r.json())

    print("\n")


def create_activities_for_user():
    activities = [
        {
            "title": "Built a Python API Server using FastAPI and Docker",
            "description": "Building a Python API Server using FastAPI and Docker to get Narrative launched",
            "category": "Achievement",
            "status": "Completed",
            "organization": "Narrative",
        },
        {
            "title": "User Testing for Narrative Launch",
            "description": "Working on user testing for Narrative launch by testing DB tables, edge cases, and integrations",
            "category": "Skill",
            "status": "In Progress",
            "organization": "Narrative",
        },
        {
            "title": "Deployed a Scalable Microservices Architecture on AWS ECS",
            "description": "Designed and deployed a scalable microservices architecture using AWS ECS, ALB, and Route 53 for Narrative's backend infrastructure.",
            "category": "Achievement",
            "status": "Completed",
            "organization": "Google",
        },
        {
            "title": "Developing CI/CD Pipelines with GitHub Actions",
            "description": "Implementing CI/CD pipelines using GitHub Actions to automate the deployment of Narrative's backend services.",
            "category": "Skill",
            "status": "In Progress",
            "organization": "Google",
        },
        {
            "title": "Optimized Database Queries for Supabase",
            "description": "Improving database performance by optimizing complex queries and indexing strategies in Supabase Postgres for Narrative.",
            "category": "Achievement",
            "status": "Completed",
            "organization": "Google",
        },
        {
            "title": "Conducting Security Audits for FastAPI Backend",
            "description": "Performing security audits on FastAPI backend services to ensure robust protection against common vulnerabilities.",
            "category": "Skill",
            "status": "In Progress",
            "organization": "Supabase",
        },
        {
            "title": "Integrated Object Storage with Supabase",
            "description": "Adding and configuring an object store in Supabase for handling large media files in Narrative's backend system.",
            "category": "Achievement",
            "status": "Completed",
            "organization": "Supabase",
        },
        {
            "title": "Dockerizing FastAPI Applications",
            "description": "Creating Docker containers for FastAPI applications to streamline the deployment process across multiple environments.",
            "category": "Skill",
            "status": "Completed",
            "organization": "Supabase",
        },
        {
            "title": "Improving API Documentation with Swagger",
            "description": "Enhancing the API documentation for FastAPI endpoints using Swagger to improve developer experience.",
            "category": "Achievement",
            "status": "Completed",
            "organization": "Personal",
        },
        {
            "title": "Load Testing and Performance Tuning",
            "description": "Conducting load testing and performance tuning on the Narrative API to ensure high availability and reliability.",
            "category": "Skill",
            "status": "In Progress",
            "organization": "Personal",
        },
        {
            "title": "Implementing OAuth2 Authentication in FastAPI",
            "description": "Integrating OAuth2 authentication to secure API endpoints in the FastAPI application for Narrative.",
            "category": "Achievement",
            "status": "Completed",
            "organization": "Personal",
        },
        {
            "title": "Refactoring Legacy Code for Scalability",
            "description": "Refactoring legacy code to improve scalability and maintainability of Narrative's backend services.",
            "category": "Skill",
            "status": "In Progress",
            "organization": "Personal",
        },
    ]
    data = {"user_id": "755a6e7c-69ca-4acb-b608-73e745e8d28d", "activities": activities}

    r = requests.post("https://backend.prod.yournarrative.io/v1/activities/insertActivities/", json=data)
    print_response(r, "create_activities_for_user")


# def create_activites_from_check_in():
#     data = {
#         "dialogue": [
#             "Tell me about what you accomplished this week. Anything you’re proud of?",
#             "I finished a project at work to scrape all of the news websites for the latest news and display it in a dashboard. I’m proud of how it turned out. I used python and selenium.",
#             "What are you working on right now?",
#             "I'm working on a new personal project to build an API server for a new company called Narrative. It's build using Python and FastAPI and Docker."
#             "What are you learning right now?",
#             "Focusing on the catching up with the latest trends in web development and server security practices.",
#         ]
#     }
#
#     r = requests.post("http://0.0.0.0:5001/api-v1/brag-doc/createActivitiesFromCheckIn/", json=data)
#     print_response(r, "create_activites_from_check_in", print_json=True)


def run_tests():
    pass
    # create_activities_for_user()
    # create_brag_doc(user_id)
    # get_brag_doc_for_user(user_id)
    # create_activites_from_check_in()


if __name__ == "__main__":
    run_tests()
