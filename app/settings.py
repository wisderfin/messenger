from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    CORS_ORIGINS: List[str]

    class Config:
        env_file = '.env'
        extra = "ignore"

settings = Settings()
