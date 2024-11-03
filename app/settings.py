from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # cors
    CORS_ORIGINS: List[str]

    # database
    DATABASE_DRIVER: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_PORT_FROM: str
    DATABASE_PORT_TO: str
    DATABASE_HOST: str

    # jwt
    JWT_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE: int
    JWT_REFRESH_TOKEN_EXPIRE: int

    # bcrypt
    BCRYPT_ROUNDS: int

    class Config:
        env_file = '.env'
        extra = "ignore"

settings = Settings()
