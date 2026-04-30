from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://musicapp:musicapp123@db:5432/musicdb"
    
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

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()