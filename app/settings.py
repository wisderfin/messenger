from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CORS_ORIGINS: List[str]
    DATABASE_DRIVER: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_PORT_FROM: str
    DATABASE_PORT_TO: str
    DATABASE_HOST: str

    class Config:
        env_file = '.env'
        extra = "ignore"

settings = Settings()
