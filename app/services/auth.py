from bcrypt import hashpw, checkpw, gensalt
from jwt import encode, decode
from datetime import datetime, timedelta, timezone

from app import settings


def hash_password(password: str) -> bytes:
    return hashpw(password.encode(), gensalt(rounds=settings.BCRYPT_ROUNDS))

def check_password(password: str, hashed_password: bytes) -> bool:
    return checkpw(password.encode(), hashed_password)

def get_access_token_jwt(data: dict) -> str:
    payload = data.copy()
    payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE)
    access_token = encode(payload, settings.JWT_KEY, algorithm=settings.JWT_ALGORITHM)
    return access_token

def get_refresh_token_jwt(data: dict) -> str:
    payload = data.copy()
    payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE)
    refresh_token = encode(payload, settings.JWT_KEY, algorithm=settings.JWT_ALGORITHM)
    return refresh_token

def decode_jwt(token: str) -> dict:
    return decode(token, settings.JWT_KEY, algorithms=[settings.JWT_ALGORITHM])
