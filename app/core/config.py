import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from datetime import timedelta

class Settings(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"  # 실제 운영환경에서는 안전한 키로 변경
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