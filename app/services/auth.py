from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from bcrypt import hashpw, checkpw, gensalt
from jwt import encode, decode
from fastapi import Response

from app.core.settings import settings

# TODO: make a function for cheked jwt


def hash_password(password: str) -> str:
    return hashpw(password.encode(), gensalt(rounds=settings.BCRYPT_ROUNDS)).decode()


def check_password(password: str, hashed_password: str) -> bool:
    return checkpw(password.encode(), hashed_password.encode())


async def get_jwt(name: str, key: str, exp: int) -> str:  # TODO: think about scheme
    current_time = datetime.now(timezone.utc)
    expire_time = timedelta(minutes=exp)
    token = encode(
        {"iss": "messenger_auth", "user": name, "exp": current_time + expire_time},
        settings.JWT_ACCESS_KEY,
        settings.JWT_ALGORITHM,
    )
    return token


async def update_jwt(
    access: str, refresh: str, session: AsyncSession
) -> tuple[str | None, str | None]:
    payload = decode(
        access, settings.JWT_ACCESS_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    user = payload.get("user")
    from app.repositories.auth import UsersUtils

    user = await UsersUtils(session).get(user)

    if user is None:
        new_acces_token = None
    # TODO: make checked existence in database
    else:
        new_acces_token = await get_jwt(
            user.username, settings.JWT_ACCESS_KEY, settings.JWT_ACCESS_TOKEN_EXPIRE
        )

    current_time = datetime.now(timezone.utc)
    exp = decode(
        refresh, settings.JWT_REFRESH_KEY, algorithms=[settings.JWT_ALGORITHM]
    ).get("exp")

    if exp < current_time.timestamp():
        new_refresh_token = None
    else:
        expire_time = timedelta(minutes=settings.JWT_REFRSH_TOKEN_EXPIRE)
        new_refresh_token = encode(
            {
                "iss": "messenger_auth",
                "user": user.username,
                "exp": current_time + expire_time,
            },
            settings.JWT_REFRESH_KEY,
            settings.JWT_ALGORITHM,
        )
    return new_acces_token, new_refresh_token


async def set_refresh_coockie(
    response: Response,
    value: str,
) -> None:
    response.set_cookie(
        key=settings.COOCKIE_JWT_REFRESH_KEY,
        value=value,
        httponly=True,
        max_age=settings.JWT_REFRESH_TOKEN_EXPIRE,
        secure=True,
        samesite="lax",
    )
