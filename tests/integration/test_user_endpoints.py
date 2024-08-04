import random
import string

import pytest
from integration.conftest import TEST_USER_EMAIL, TEST_USER_UUID

from information_retrieval.api.v1.routers.activity import insert_activities_endpoint
from information_retrieval.api.v1.routers.user import (
    get_all_organizations_for_user_endpoint,
    get_user_profile_data_endpoint,
    update_user_profile_data_endpoint,
)


def random_string(length=10):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


@pytest.mark.usefixtures("setup_class_fixture")
class TestUsersEndpoints:
    def test_get_user_data(self):
        request_data = {"user_id": TEST_USER_UUID}
        response = self.user_client.post(get_user_profile_data_endpoint, json=request_data)
        assert response.status_code == 200

        user_data = response.json()["user_data"]
        assert user_data["user_id"] == TEST_USER_UUID
        assert user_data["email"] == TEST_USER_EMAIL

    def test_update_user_data(self):
        # Get current user data
        get_request_data = {"user_id": TEST_USER_UUID}
        get_response = self.user_client.post(get_user_profile_data_endpoint, json=get_request_data)
        assert get_response.status_code == 200

        # Create random data for update
        random_bio = random_string()
        random_linkedin_url = f"https://linkedin.com/in/{random_string()}"
        user_data = get_response.json()["user_data"]
        user_data["bio"] = random_bio
        user_data["linkedin_profile_url"] = random_linkedin_url

        # Update user data
        update_request_data = {"user_data": user_data}
        update_response = self.user_client.post(update_user_profile_data_endpoint, json=update_request_data)
        assert update_response.status_code == 200

        # Get updated user data to verify changes
        verify_response = self.user_client.post(get_user_profile_data_endpoint, json=get_request_data)
        assert verify_response.status_code == 200

        updated_user_data = verify_response.json()["user_data"]
        assert updated_user_data["bio"] == random_bio
        assert updated_user_data["linkedin_profile_url"] == random_linkedin_url

    def test_get_all_organizations_for_a_user(self):
        o1 = "Organization 1"
        o2 = "Organization 2"
        o3 = "Organization 3"

        data = {
            "user_id": TEST_USER_UUID,
            "activities": [
                {
                    "title": "Title 1",
                    "description": "Description 1",
                    "category": "Achievement",
                    "status": "In Progress",
                    "organization": o1,
                },
                {
                    "title": "Title 2",
                    "description": "Description 2",
                    "category": "Achievement",
                    "status": "In Progress",
                    "organization": o2,
                },
                {
                    "title": "Title 3",
                    "description": "Description 3",
                    "category": "Achievement",
                    "status": "In Progress",
                    "organization": o3,
                },
                {
                    "title": "Title 4",
                    "description": "Description 3",
                    "category": "Achievement",
                    "status": "In Progress",
                },
            ],
        }
        response = self.user_client.post(insert_activities_endpoint, json=data)
        assert response.status_code == 200

        # Verify data in the database
        activities = self.supabase_client.table("activities").select("*").eq("user_id", TEST_USER_UUID).execute().data
        assert len(activities) == 4

        # Get all organizations for the user
        response = self.user_client.post(get_all_organizations_for_user_endpoint, json=data)
        assert response.status_code == 200
        assert set(response.json().get("organizations")) == {o1, o2, o3}
