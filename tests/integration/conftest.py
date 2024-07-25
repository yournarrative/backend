import os
import uuid

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

# DO NOT CHANGE THIS TO PROD OR YOU WILL DELETE EVERYTHING :)
# Need to be loaded before FastAPI app is imported to load env properly
load_dotenv("resources/config/local/local.env")

from information_retrieval.connectors.supabase.client import create_supabase_client
from information_retrieval.main import app

# TEST DATA CONSTANTS
TEST_USER_EMAIL: str = "shayaan.jagtap@gmail.com"
TEST_USER_UUID: str = "b945a7c8-171f-454f-b6f8-e42d778fd889"


@pytest.fixture(scope="session")
def user_client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def supabase_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    return create_supabase_client(url, key)


@pytest.fixture(scope="class", autouse=True)
def setup_class_fixture(request, supabase_client, user_client):
    request.cls.user_client = user_client
    request.cls.supabase_client = supabase_client


@pytest.fixture(scope="function", autouse=True)
def clear_supabase_data(supabase_client):
    # Check if this is prod
    PROD_URL_STRING = "vvlnagr"
    if PROD_URL_STRING in os.environ.get("SUPABASE_URL"):
        print("DOUBLE CHECK THAT YOU'RE NOT ABOUT TO DELETE THE PROD DB")
        raise ValueError("Do not delete prod db please")
    # List all tables and clear the data - hardcoded because query to information schema isn't working idk
    # Do not delete "activity_category_options", "activity_status_options", or "profiles" table
    table_names = ["activities", "brag_docs", "check_ins"]

    # Extract table names from the result
    for table_name in table_names:
        supabase_client.table(table_name).delete().neq(
            "id", uuid.UUID("00000000-0000-0000-0000-000000000000")
        ).execute()
    yield
