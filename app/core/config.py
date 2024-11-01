import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from datetime import timedelta

class Settings(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "c8e916d5f7a7afe4f9d2f6b1c3a4d5e8b7f9c2e5d8a1b4f7c0e3d6a9b2f5c8e"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = f".env.{os.getenv('ENV', 'development')}"
        env_file_encoding = 'utf-8'
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 