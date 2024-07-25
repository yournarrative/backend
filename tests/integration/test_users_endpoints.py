import pytest
from integration.conftest import TEST_USER_EMAIL, TEST_USER_UUID

from information_retrieval.api.v1.routers.users import get_user_data_endpoint


@pytest.mark.usefixtures("setup_class_fixture")
class TestUsersEndpoints:
    def test_get_user_data(self):
        request_data = {"user_id": TEST_USER_UUID}
        response = self.user_client.post(get_user_data_endpoint, json=request_data)
        assert response.status_code == 200

        user_data = response.json()["user_data"]
        assert user_data["user_id"] == TEST_USER_UUID
        assert user_data["email"] == TEST_USER_EMAIL
