import pytest
from integration.conftest import TEST_USER_UUID

from information_retrieval.api.v1.routers.activity import (
    create_activities_from_check_in_endpoint,
    delete_activities_endpoint,
    get_activities_endpoint,
    get_activities_for_display_endpoint,
    insert_activities_endpoint,
    update_activity_with_new_details_endpoint,
    upsert_activity_endpoint,
)


@pytest.mark.usefixtures("setup_class_fixture")
class TestActivitiesEndpoints:
    def test_insert_activities(self):
        title = "Some Title"
        description = "Some description"
        data = {
            "user_id": TEST_USER_UUID,
            "activities": [
                {"title": title, "description": description, "category": "Achievement", "status": "In Progress"}
            ],
        }
        response = self.user_client.post(insert_activities_endpoint, json=data)
        assert response.status_code == 200

        # Verify data in the database
        activities = self.supabase_client.table("activities").select("*").eq("user_id", TEST_USER_UUID).execute().data
        assert len(activities) == 1
        assert activities[0]["title"] == title
        assert activities[0]["description"] == description
        assert activities[0]["category"] == "Achievement"
        assert activities[0]["status"] == "In Progress"

    def test_insert_multiple_activities(self):
        data = {
            "user_id": TEST_USER_UUID,
            "activities": [
                {
                    "title": "Title 1",
                    "description": "Description 1",
                    "category": "Achievement",
                    "status": "In Progress",
                },
                {
                    "title": "Title 2",
                    "description": "Description 2",
                    "category": "Achievement",
                    "status": "In Progress",
                },
                {
                    "title": "Title 3",
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
        assert len(activities) == 3

    def test_delete_activities(self):
        # First, insert an activity to delete
        insert_data = {
            "user_id": TEST_USER_UUID,
            "activities": [
                {
                    "title": "activity1",
                    "description": "some description",
                    "category": "Achievement",
                    "status": "In Progress",
                }
            ],
        }
        self.user_client.post(insert_activities_endpoint, json=insert_data)

        # Delete the activity
        activity_id_list = [
            self.supabase_client.table("activities").select("id").eq("user_id", TEST_USER_UUID).execute().data[0]["id"]
        ]
        delete_data = {"activity_id_list": activity_id_list}
        response = self.user_client.post(delete_activities_endpoint, json=delete_data)
        assert response.status_code == 200

        # Verify data in the database
        activities = (
            self.supabase_client.table("activities")
            .select("*")
            .eq("user_id", TEST_USER_UUID)
            .eq("deleted", False)
            .execute()
            .data
        )
        assert len(activities) == 0

    def test_get_activities_for_user(self):
        # First, insert an activity
        insert_data = {
            "user_id": TEST_USER_UUID,
            "activities": [
                {
                    "title": "activity1",
                    "description": "some description",
                    "category": "Achievement",
                    "status": "In Progress",
                }
            ],
        }
        self.user_client.post(insert_activities_endpoint, json=insert_data)

        request_data = {"user_id": TEST_USER_UUID}
        response = self.user_client.post(get_activities_endpoint, json=request_data)
        assert response.status_code == 200
        activities = response.json()["activities"]
        assert len(activities) == 1
        assert activities[0]["title"] == "activity1"
        assert activities[0]["description"] == "some description"
        assert activities[0]["category"] == "Achievement"
        assert activities[0]["status"] == "In Progress"

    def test_update_activity(self):
        # First, insert an activity
        insert_data = {
            "user_id": TEST_USER_UUID,
            "activities": [
                {
                    "title": "activity1",
                    "description": "some description",
                    "category": "Achievement",
                    "status": "In Progress",
                }
            ],
        }
        self.user_client.post(insert_activities_endpoint, json=insert_data)

        # Get the activity ID
        activity_id = (
            self.supabase_client.table("activities").select("id").eq("user_id", TEST_USER_UUID).execute().data[0]["id"]
        )

        # Update the activity
        update_data = {
            "activity_with_id": {
                "id": activity_id,
                "title": "activity1",
                "description": "updated description",
                "category": "Achievement",
                "status": "Completed",
            }
        }
        response = self.user_client.post(upsert_activity_endpoint, json=update_data)
        assert response.status_code == 200

        # Verify the updated data in the database
        activities = self.supabase_client.table("activities").select("*").eq("id", activity_id).execute().data
        assert len(activities) == 1
        assert activities[0]["description"] == "updated description"
        assert activities[0]["status"] == "Completed"

    def test_update_activity_with_new_details(self):
        # First, insert an activity
        insert_data = {
            "user_id": TEST_USER_UUID,
            "activities": [
                {
                    "title": "Learning How to Unit Test Using Pytest",
                    "description": "Working on an end to end setup to do "
                    "integration testing using Pytest for a FastAPI app in Python",
                    "category": "Achievement",
                    "status": "In Progress",
                }
            ],
        }
        self.user_client.post(insert_activities_endpoint, json=insert_data)

        # Get the activity ID
        activity_id = (
            self.supabase_client.table("activities").select("id").eq("user_id", TEST_USER_UUID).execute().data[0]["id"]
        )

        # Update the activity with new details
        update_data = {"activity_id": str(activity_id), "update": "I completed the Unit Testing in Python using Pytest"}
        response = self.user_client.post(update_activity_with_new_details_endpoint, json=update_data)
        assert response.status_code == 200
        updated_activity = response.json()
        assert updated_activity["activity_with_id"]["status"] == "Completed"

        # Upsert new activity data
        response = self.user_client.post(upsert_activity_endpoint, json=updated_activity)
        assert response.status_code == 200

        # Verify the updated data in the database
        updated_activities = self.supabase_client.table("activities").select("*").eq("id", activity_id).execute().data
        assert len(updated_activities) == 1
        assert updated_activities[0]["category"] == updated_activity["activity_with_id"]["category"]
        assert updated_activities[0]["title"] == updated_activity["activity_with_id"]["title"]
        assert updated_activities[0]["description"] == updated_activity["activity_with_id"]["description"]
        assert updated_activities[0]["status"] == updated_activity["activity_with_id"]["status"]

    def test_create_activities_from_check_in(self):
        # Mock dialogue data
        dialogue_data = {
            "dialogue": [
                "What did you learn or accomplish this week?",
                "Today I completed the unit testing for the FastAPI application for my job at Acme Corp "
                "and started the integration testing for a personal project.",
            ]
        }

        response = self.user_client.post(create_activities_from_check_in_endpoint, json=dialogue_data)
        assert response.status_code == 200

        response_data = response.json()
        assert "activities" in response_data
        assert len(response_data["activities"]) == 2
        assert "Acme Corp" in [a["organization"] for a in response_data["activities"]]

    def test_create_activities_from_check_in_empty_dialogue(self):
        dialogue_data = {"dialogue": []}

        response = self.user_client.post(create_activities_from_check_in_endpoint, json=dialogue_data)
        assert response.status_code == 200
        assert response.json().get("activities") == []

    def test_create_activities_from_check_in_empty_strings(self):
        dialogue_data = {"dialogue": [""]}

        response = self.user_client.post(create_activities_from_check_in_endpoint, json=dialogue_data)
        assert response.status_code == 200
        assert response.json().get("activities") == []

    def test_create_activities_from_check_in_empty_responses(self):
        dialogue_data = {"dialogue": ["What did you learn or accomplish this week?", ""]}

        response = self.user_client.post(create_activities_from_check_in_endpoint, json=dialogue_data)
        assert response.status_code == 200
        assert response.json().get("activities") == []

    def test_create_activities_from_check_in_nonsense_dialogue(self):
        dialogue_data = {"dialogue": ["What did you learn or accomplish recently?", " ".join(["activity"] * 1000)]}

        response = self.user_client.post(create_activities_from_check_in_endpoint, json=dialogue_data)
        assert response.status_code == 200
        assert response.json().get("activities") == []

    def test_create_activities_from_check_in_ambiguous_dialogue(self):
        dialogue_data = {"dialogue": ["What did you learn or accomplish recently?", "I did a lot of stuff today."]}

        response = self.user_client.post(create_activities_from_check_in_endpoint, json=dialogue_data)
        assert response.status_code == 200
        assert response.json().get("activities") == []

    def test_get_activities_for_display(self):
        # First, insert some activities associated with different organizations
        insert_data = {
            "user_id": TEST_USER_UUID,
            "activities": [
                {
                    "title": "Learned Python Basics",
                    "description": "Took a 6 month intensive course to learn python basics, including data structures and algorithms",
                    "category": "Skill",
                    "status": "Completed",
                    "organization": "Personal",
                },
                {
                    "title": "Building Personal Website",
                    "description": "Building a personal website in Javascript and python using Django",
                    "category": "Achievement",
                    "status": "In Progress",
                    "organization": "Personal",
                },
                {
                    "title": "Learned how to manage a team",
                    "description": "Read 3 books on team management and took over a small project, overseeing a team of 5 developers",
                    "category": "Skill",
                    "status": "Completed",
                    "organization": "Acme Corp",
                },
                {
                    "title": "Learned how deploy a production service",
                    "description": "Released a 6 month project to production, including setting up CI/CD pipelines and monitoring",
                    "category": "Skill",
                    "status": "Completed",
                    "organization": "Acme Corp",
                },
            ],
        }

        self.user_client.post(insert_activities_endpoint, json=insert_data)

        # Request activities for display without summaries
        request_data = {"user_id": TEST_USER_UUID, "include_summaries": True}
        response = self.user_client.post(get_activities_for_display_endpoint, json=request_data)
        assert response.status_code == 200

        response_data = response.json()

        assert "user_organization_data_map" in response_data
        assert len(response_data["user_organization_data_map"]) == 2  # Two organizations
        assert "Acme Corp" in response_data["user_organization_data_map"]
        assert "Personal" in response_data["user_organization_data_map"]

        assert "user_organization_data_map" in response_data
        assert len(response_data["user_organization_data_map"]) == 2  # Two organizations

        # Verify that summaries are included
        personal = response_data["user_organization_data_map"]["Personal"]
        assert len(personal["activities"]) == 2
        assert len(personal["summary"]) > 0  # Summary should not be empty

        acme_data = response_data["user_organization_data_map"]["Acme Corp"]
        assert len(acme_data["activities"]) == 2
        assert len(acme_data["summary"]) > 0  # Summary should not be empty

    def test_get_activities_for_display_empty_user(self):
        # Request activities for a user with no activities
        request_data = {"user_id": "nonexistent-user-id", "include_summaries": False}
        response = self.user_client.post(get_activities_for_display_endpoint, json=request_data)
        assert response.status_code == 200

        response_data = response.json()
        assert "user_organization_data_map" in response_data
        assert len(response_data["user_organization_data_map"]) == 0  # No organizations

    def test_get_activities_for_display_with_no_organizations(self):
        # Insert activities without any organization
        insert_data = {
            "user_id": TEST_USER_UUID,
            "activities": [
                {
                    "title": "activity1",
                    "description": "some description",
                    "category": "Achievement",
                    "status": "In Progress",
                }
            ],
        }
        self.user_client.post(insert_activities_endpoint, json=insert_data)

        # Request activities for display
        request_data = {"user_id": TEST_USER_UUID, "include_summaries": False}
        response = self.user_client.post(get_activities_for_display_endpoint, json=request_data)
        assert response.status_code == 200

        response_data = response.json()
        assert "user_organization_data_map" in response_data
        assert len(response_data["user_organization_data_map"]) == 1  # We should default to "Personal" as organization

    def test_get_activities_for_display_invalid_user_id(self):
        # Request activities with an invalid user ID
        request_data = {"user_id": 12345, "include_summaries": False}  # User ID should be a string
        response = self.user_client.post(get_activities_for_display_endpoint, json=request_data)
        assert response.status_code == 422  # Expecting validation error
