import os
from io import BytesIO

import pytest
from integration.conftest import TEST_USER_UUID

from information_retrieval.api.v1.routers.files import (
    extract_activities_from_resume_endpoint,
    get_profile_picture_endpoint,
    get_resume_endpoint,
    upload_profile_picture_endpoint,
    upload_resume_endpoint,
)


@pytest.mark.usefixtures("setup_class_fixture")
class TestUploadResumeEndpoint:
    @pytest.fixture(autouse=True)
    def setup(self, user_client, supabase_client):
        self.user_client = user_client
        self.supabase_client = supabase_client

    def test_upload_valid_real_pdf(self):
        file_path = os.path.join("tests", "resources", "resumes", "ShayaanResume.pdf")
        with open(file_path, "rb") as f:
            file_content = f.read()

        files = {"file": ("ShayaanResume.pdf", BytesIO(file_content), "application/pdf")}
        data = {"user_id": TEST_USER_UUID, "file_name": "ShayaanResume.pdf"}  # Include file_name in data

        response = self.user_client.post(upload_resume_endpoint, files=files, data=data)
        assert response.status_code == 200

    def test_upload_empty_file(self):
        files = {"file": ("empty_resume.pdf", BytesIO(b""), "application/pdf")}
        data = {"user_id": TEST_USER_UUID, "file_name": "empty_resume.pdf"}  # Include file_name in data

        response = self.user_client.post(upload_resume_endpoint, files=files, data=data)
        assert response.status_code == 400
        assert response.json() == {"detail": "Empty file"}

    def test_upload_missing_file(self):
        data = {"user_id": TEST_USER_UUID, "file_name": "missing_resume.pdf"}  # Include file_name in data

        response = self.user_client.post(upload_resume_endpoint, files={}, data=data)
        assert response.status_code == 422  # Unprocessable Entity due to missing file
        assert "file" in response.json()["detail"][0]["loc"]

    def test_upload_invalid_file_type(self):
        file_content = b"Invalid content"
        files = {"file": ("resume.txt", BytesIO(file_content), "text/plain")}
        data = {"user_id": TEST_USER_UUID, "file_name": "resume.txt"}  # Include file_name in data

        response = self.user_client.post(upload_resume_endpoint, files=files, data=data)
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid file type"}

    def test_upload_large_file(self):
        large_content = b"%PDF-1.4\n%..." + b"A" * (5 * 1024 * 1024 + 1)  # Just over 5 MB
        files = {"file": ("large_resume.pdf", BytesIO(large_content), "application/pdf")}
        data = {"user_id": TEST_USER_UUID, "file_name": "large_resume.pdf"}  # Include file_name in data

        response = self.user_client.post(upload_resume_endpoint, files=files, data=data)
        assert response.status_code == 413
        assert response.json() == {"detail": "File too large"}

    def test_fetch_activities_from_resume_success(self):
        # Ensure the resume is uploaded first
        with open(os.path.join("tests", "resources", "resumes", "ShayaanResume.pdf"), "rb") as f:
            file_content = f.read()
        files = {"file": ("resume.pdf", BytesIO(file_content), "application/pdf")}
        data = {"user_id": TEST_USER_UUID, "file_name": "ShayaanResume.pdf"}
        upload_response = self.user_client.post(upload_resume_endpoint, files=files, data=data)
        assert upload_response.status_code == 200

        # Now fetch the resume and extract activities
        fetch_data = {"user_id": TEST_USER_UUID}
        fetch_response = self.user_client.post(extract_activities_from_resume_endpoint, json=fetch_data)
        assert fetch_response.status_code == 200
        assert "activities" in fetch_response.json()
        assert isinstance(fetch_response.json()["activities"], list)
        assert len(fetch_response.json()["activities"]) > 0

    def test_fetch_resume_file_not_found(self):
        # Attempt to fetch a resume that doesn't exist
        fetch_data = {"user_id": "non-existent-user-id"}
        fetch_response = self.user_client.post(get_resume_endpoint, json=fetch_data)
        assert fetch_response.status_code == 500
        assert fetch_response.json() == {"detail": "Error fetching requested resume from file storage"}

    def test_fetch_existing_resume(self):
        # Assume the resume was uploaded first
        with open(os.path.join("tests", "resources", "resumes", "ShayaanResume.pdf"), "rb") as f:
            file_content = f.read()
        files = {"file": ("ShayaanResume.pdf", BytesIO(file_content), "application/pdf")}
        data = {"user_id": TEST_USER_UUID, "file_name": "ShayaanResume.pdf"}  # Include file_name in data
        upload_response = self.user_client.post(upload_resume_endpoint, files=files, data=data)
        assert upload_response.status_code == 200

        # Fetch the resume
        fetch_data = {"user_id": TEST_USER_UUID}
        fetch_response = self.user_client.post(get_resume_endpoint, json=fetch_data)
        assert fetch_response.status_code == 200
        assert fetch_response.headers["Content-Disposition"] == "attachment; filename=ShayaanResume.pdf"
        assert fetch_response.headers["Content-Type"] == "application/pdf"
        assert fetch_response.content == file_content

    def test_fetch_resume_missing_user_id(self):
        fetch_data = {}
        fetch_response = self.user_client.post(get_resume_endpoint, json=fetch_data)
        assert fetch_response.status_code == 422  # Unprocessable Entity due to missing user_id
        assert "user_id" in fetch_response.json()["detail"][0]["loc"]

    def test_upload_missing_file_name(self):
        file_path = os.path.join("tests", "resources", "resumes", "ShayaanResume.pdf")
        with open(file_path, "rb") as f:
            file_content = f.read()

        files = {"file": ("ShayaanResume.pdf", BytesIO(file_content), "application/pdf")}
        data = {"user_id": TEST_USER_UUID}  # No file_name provided

        response = self.user_client.post(upload_resume_endpoint, files=files, data=data)
        assert response.status_code == 422
        assert "file_name" in response.json()["detail"][0]["loc"]


@pytest.mark.usefixtures("setup_class_fixture")
class TestUploadProfilePictureEndpoint:
    @pytest.fixture(autouse=True)
    def setup(self, user_client, supabase_client):
        self.user_client = user_client
        self.supabase_client = supabase_client

    def test_upload_valid_image_jpeg(self):
        file_path = os.path.join("tests", "resources", "images", "profile_picture.jpeg")
        with open(file_path, "rb") as f:
            file_content = f.read()

        files = {"file": ("profile_picture.jpeg", BytesIO(file_content), "image/jpeg")}
        data = {"user_id": TEST_USER_UUID}

        response = self.user_client.post(upload_profile_picture_endpoint, files=files, data=data)
        assert response.status_code == 200

    def test_upload_valid_image_png(self):
        file_path = os.path.join("tests", "resources", "images", "profile_picture.png")
        with open(file_path, "rb") as f:
            file_content = f.read()

        files = {"file": ("profile_picture.png", BytesIO(file_content), "image/png")}
        data = {"user_id": TEST_USER_UUID}

        response = self.user_client.post(upload_profile_picture_endpoint, files=files, data=data)
        assert response.status_code == 200

    def test_upload_invalid_file_type_image(self):
        file_content = b"Invalid image content"
        files = {"file": ("invalid_image.txt", BytesIO(file_content), "text/plain")}
        data = {"user_id": TEST_USER_UUID}

        response = self.user_client.post(upload_profile_picture_endpoint, files=files, data=data)
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid file type"}

    def test_upload_empty_image_file(self):
        files = {"file": ("empty_image.jpg", BytesIO(b""), "image/jpeg")}
        data = {"user_id": TEST_USER_UUID}

        response = self.user_client.post(upload_profile_picture_endpoint, files=files, data=data)
        assert response.status_code == 400
        assert response.json() == {"detail": "Empty file"}

    def test_fetch_existing_profile_picture_jpeg(self):
        # Assume the profile picture was uploaded first
        file_path = os.path.join("tests", "resources", "images", "profile_picture.jpeg")
        with open(file_path, "rb") as f:
            file_content = f.read()

        files = {"file": ("profile_picture.jpeg", BytesIO(file_content), "image/jpeg")}
        data = {"user_id": TEST_USER_UUID}
        upload_response = self.user_client.post(upload_profile_picture_endpoint, files=files, data=data)
        assert upload_response.status_code == 200

        # Fetch the profile picture
        fetch_data = {"user_id": TEST_USER_UUID}
        fetch_response = self.user_client.post(get_profile_picture_endpoint, json=fetch_data)
        assert fetch_response.status_code == 200
        assert fetch_response.headers["Content-Disposition"] == "attachment; filename=profile_picture.jpeg"
        assert fetch_response.headers["Content-Type"] == "image/jpeg"
        assert len(fetch_response.content) > 0

    def test_fetch_existing_profile_picture_png(self):
        # Assume the profile picture was uploaded first
        file_path = os.path.join("tests", "resources", "images", "profile_picture.png")
        with open(file_path, "rb") as f:
            file_content = f.read()

        files = {"file": ("profile_picture.pg", BytesIO(file_content), "image/png")}
        data = {"user_id": TEST_USER_UUID}
        upload_response = self.user_client.post(upload_profile_picture_endpoint, files=files, data=data)
        assert upload_response.status_code == 200

        # Fetch the profile picture
        fetch_data = {"user_id": TEST_USER_UUID}
        fetch_response = self.user_client.post(get_profile_picture_endpoint, json=fetch_data)
        assert fetch_response.status_code == 200
        assert fetch_response.headers["Content-Disposition"] == "attachment; filename=profile_picture.jpeg"
        assert fetch_response.headers["Content-Type"] == "image/jpeg"
        assert len(fetch_response.content) > 0

    def test_fetch_non_existent_profile_picture(self):
        fetch_data = {"user_id": "non-existent-user-id"}
        fetch_response = self.user_client.post(get_profile_picture_endpoint, json=fetch_data)
        assert fetch_response.status_code == 500
        assert fetch_response.json() == {"detail": "Error fetching requested profile picture from file storage"}

    def test_fetch_profile_picture_missing_user_id(self):
        fetch_data = {}
        fetch_response = self.user_client.post(get_profile_picture_endpoint, json=fetch_data)
        assert fetch_response.status_code == 422
