import boto3
from typing import Optional
from app.core.config import settings


class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION,
        )
        self.bucket = settings.AWS_STORAGE_BUCKET_NAME

    def upload_file(self, file_obj, file_name: str, content_type: str) -> Optional[str]:
        """Upload file to S3, return public URL or None."""
        try:
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket,
                file_name,
                ExtraArgs={"ContentType": content_type},
            )
            if settings.AWS_S3_CUSTOM_DOMAIN:
                return f"{settings.AWS_S3_CUSTOM_DOMAIN}/{file_name}"
            return f"https://{self.bucket}.s3.{settings.AWS_S3_REGION}.amazonaws.com/{file_name}"
        except Exception:
            return None

    def delete_file(self, file_name: str) -> bool:
        """Delete file from S3."""
        try:
            self.s3_client.delete_object(Bucket=self.bucket, Key=file_name)
            return True
        except Exception:
            return False
