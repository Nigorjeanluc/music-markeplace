from unittest.mock import Mock, patch, MagicMock
import pytest
from fastapi import UploadFile


def test_upload_file_success():
    """Test successful S3 upload returns URL."""
    with patch("app.services.s3_service.boto3") as mock_boto3:
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client

        from app.services.s3_service import S3Service
        service = S3Service()

        url = service.upload_file("fake_file_obj", "artists/test.jpg", "image/jpeg")

        assert url is not None
        assert "test.jpg" in url
        mock_client.upload_fileobj.assert_called_once()


def test_upload_file_failure():
    """Test S3 upload failure returns None."""
    with patch("app.services.s3_service.boto3") as mock_boto3:
        mock_client = MagicMock()
        mock_client.upload_fileobj.side_effect = Exception("S3 error")
        mock_boto3.client.return_value = mock_client

        from app.services.s3_service import S3Service
        service = S3Service()

        url = service.upload_file("fake_file", "test.jpg", "image/jpeg")
        assert url is None


def test_delete_file_success():
    """Test successful S3 delete."""
    with patch("app.services.s3_service.boto3") as mock_boto3:
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client

        from app.services.s3_service import S3Service
        service = S3Service()

        result = service.delete_file("artists/test.jpg")
        assert result is True
        mock_client.delete_object.assert_called_once_with(
            Bucket=service.bucket, Key="artists/test.jpg"
        )


def test_delete_file_failure():
    """Test S3 delete failure returns False."""
    with patch("app.services.s3_service.boto3") as mock_boto3:
        mock_client = MagicMock()
        mock_client.delete_object.side_effect = Exception("S3 error")
        mock_boto3.client.return_value = mock_client

        from app.services.s3_service import S3Service
        service = S3Service()

        result = service.delete_file("artists/test.jpg")
        assert result is False
