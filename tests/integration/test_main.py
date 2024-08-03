import pytest
from fastapi.testclient import TestClient

from information_retrieval.main import app

client = TestClient(app)


@pytest.mark.usefixtures("setup_class_fixture")
class TestMain:
    @pytest.fixture(autouse=True)
    def setup(self, user_client, supabase_client):
        self.user_client = user_client
        self.supabase_client = supabase_client

    def test_health_check(self):
        response = self.user_client.get("/")
        assert response.status_code == 200
        assert response.json() == "I'm healthy, yo!"
