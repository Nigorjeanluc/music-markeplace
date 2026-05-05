from pydantic_settings import BaseSettings
from pydantic import ConfigDict, field_validator
from typing import List
from pathlib import Path
import json
import os


class Settings(BaseSettings):
    # Database - no default to force using environment variable
    DATABASE_URL: str
    DATABASE_URL_TEST: str = ""

    @field_validator("DATABASE_URL", "DATABASE_URL_TEST")
    @classmethod
    def validate_db_url(cls, v: str) -> str:
        """Convert postgres:// to postgresql:// for SQLAlchemy compatibility."""
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

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

    # CORS - read as string, parsed in get_allowed_origins()
    ALLOWED_ORIGINS: str = ""

    def get_allowed_origins(self) -> List[str]:
        """Parse ALLOWED_ORIGINS from JSON array string or comma-separated string."""
        v = self.ALLOWED_ORIGINS
        if not v:
            return []
        # Try JSON first (e.g., '["https://example.com"]')
        if v.strip().startswith("["):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                pass
        # Fall back to comma-separated (e.g., 'https://example.com,https://another.com')
        return [origin.strip() for origin in v.split(",") if origin.strip()]

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

    model_config = ConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
