from bcrypt import hashpw, checkpw, gensalt
from jwt import encode, decode
from datetime import datetime, timedelta, timezone

from app import settings


def hash_password(password: str) -> bytes:
    return hashpw(password.encode(), gensalt(rounds=settings.BCRYPT_ROUNDS)).decode()

def check_password(password: str, hashed_password: bytes) -> bool:
    return checkpw(password.encode(), hashed_password)

def get_access_token_jwt(name: str) -> str:
    token = encode(
        {
            'alg': settings.JWT_ALGORITHM,
            'typ': 'JWT',
            'iss': 'messenger_auth',
            'user': name,
            'exp': settings.JWT_ACCESS_TOKEN_EXPIRE
        },
        settings.JWT_ACCESS_KEY,
        settings.JWT_ALGORITHM
    )
    return token

def get_refresh_token_jwt(data: dict) -> str:
    payload = data.copy()
    current_time = datetime.now(timezone.utc)
    refresh_expire = timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRE)
    payload['exp'] = current_time + refresh_expire
    refresh_token = encode(
        payload,
        settings.JWT_REFRESH_KEY,
        algorithm=settings.JWT_ALGORITHM
        )
    return refresh_token

def decode_jwt(token: str) -> dict:
    return decode(token, settings.JWT_KEY, algorithms=[settings.JWT_ALGORITHM])
