import pytest
from unittest.mock import patch, MagicMock


class TestUploadEndpoint:
    def test_upload_success(self, client, admin_token):
        with patch("app.services.s3_service.boto3") as mock_boto3:
            mock_client = MagicMock()
            mock_boto3.client.return_value = mock_client

            response = client.post(
                "/api/v1/upload",
                files={"file": ("test.jpg", b"fake_image_data", "image/jpeg")},
                data={"folder": "artists"},
                headers={"Authorization": f"Bearer {admin_token}"}
            )
            assert response.status_code == 200
            data = response.json()
            assert "url" in data

    def test_upload_non_image_rejected(self, client, admin_token):
        response = client.post(
            "/api/v1/upload",
            files={"file": ("test.txt", b"fake", "text/plain")},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 400
        assert "image" in response.json()["detail"].lower()

    def test_upload_unauthorized(self, client):
        response = client.post(
            "/api/v1/upload",
            files={"file": ("test.jpg", b"fake", "image/jpeg")}
        )
        assert response.status_code == 401
