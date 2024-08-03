import os
from io import BytesIO

import pytest
from integration.conftest import TEST_USER_UUID

from information_retrieval.api.v1.routers.resume import parse_resume_and_return_activities_endpoint


@pytest.mark.usefixtures("setup_class_fixture")
class TestUploadResumeEndpoint:
    @pytest.fixture(autouse=True)
    def setup(self, user_client, supabase_client):
        self.user_client = user_client
        self.supabase_client = supabase_client

    def test_upload_valid_fake_pdf(self):
        file_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 55 >>\nstream\nBT\n/F1 24 Tf\n100 100 Td\n(Hello, World!) Tj\nET\nendstream\nendobj\n5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\nxref\n0 6\n0000000000 65535 f\n0000000015 00000 n\n0000000063 00000 n\n0000000115 00000 n\n0000000178 00000 n\n0000000331 00000 n\ntrailer\n<< /Root 1 0 R /Size 6 >>\nstartxref\n391\n%%EOF"
        files = {"file": ("resume.pdf", BytesIO(file_content), "application/pdf")}
        data = {"user_id": TEST_USER_UUID}

        response = self.user_client.post(parse_resume_and_return_activities_endpoint, files=files, data=data)
        assert response.status_code == 200
        assert "activities" in response.json()
        assert isinstance(response.json()["activities"], list)

    def test_upload_valid_real_pdf(self):
        file_path = os.path.join("tests", "resources", "resumes", "ShayaanResume.pdf")
        with open(file_path, "rb") as f:
            file_content = f.read()

        files = {"file": ("ShayaanResume.pdf", BytesIO(file_content), "application/pdf")}
        data = {"user_id": TEST_USER_UUID}

        response = self.user_client.post(parse_resume_and_return_activities_endpoint, files=files, data=data)
        assert response.status_code == 200
        assert "activities" in response.json()
        assert isinstance(response.json()["activities"], list)
        # print(response.json().get("activities"))
        # assert 1 == 2

    def test_upload_invalid_file_type(self):
        file_content = b"Invalid content"
        files = {"file": ("resume.txt", BytesIO(file_content), "text/plain")}
        data = {"user_id": TEST_USER_UUID}

        response = self.user_client.post(parse_resume_and_return_activities_endpoint, files=files, data=data)
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid file type"}

    def test_upload_large_file(self):
        large_content = b"%PDF-1.4\n%..." + b"A" * (5 * 1024 * 1024 + 1)  # Just over 5 MB
        files = {"file": ("large_resume.pdf", BytesIO(large_content), "application/pdf")}
        data = {"user_id": TEST_USER_UUID}

        response = self.user_client.post(parse_resume_and_return_activities_endpoint, files=files, data=data)
        assert response.status_code == 413
        assert response.json() == {"detail": "File too large"}
