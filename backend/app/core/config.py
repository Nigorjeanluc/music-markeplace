from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List
from pathlib import Path

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://musicapp:musicapp123@db:5432/musicdb"
    DATABASE_URL_TEST: str = "postgresql://musicapp:musicapp123@db:5432/musicdb_test"

    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # URLs
    FRONTEND_URL: str | None = None
    BACKEND_URL: str | None = None

    # CORS
    ALLOWED_ORIGINS: List[str] = []  # This will be populated from the .env file as a comma-separated list

    # Project
    PROJECT_NAME: str = "Music Marketplace API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # S3 Storage
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_STORAGE_BUCKET_NAME: str = "music-marketplace-images"
    AWS_S3_CUSTOM_DOMAIN: str | None = None  # Optional CDN like CloudFront
    AWS_S3_REGION: str = "us-east-1"

    model_config = ConfigDict(env_file=Path(__file__).parent.parent / ".env", case_sensitive=True)

settings = Settings()
