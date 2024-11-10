from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated


from app.core.settings import settings
from app.infrastructure.database import get_async_session
from app.domain.repositories.auth import UserRepository
from app.domain.services.auth import (
    get_jwt,
    update_jwt,
    set_refresh_coockie,
    hash_password,
    check_password,
)
from app.api.v1.schemas.auth import (
    CreateUserScheme,
    OutputUserScheme,
    OutputJWTTokenScheme,
)


router_auth = APIRouter(prefix="/v1/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")


# TODO: OOP
@router_auth.post("/registration")
async def registration(
    user: CreateUserScheme, session: AsyncSession = Depends(get_async_session)
) -> OutputUserScheme:
    # TODO: validate email trought send code
    user_model = await UserRepository(session).create(
        user.name, user.username, user.email, user.password
    )
    return OutputUserScheme.model_validate(user_model)


@router_auth.post(
    "/login"
)  # TODO: make methods trought other services(email, google, github, ...)
async def login(
    response: Response,
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> OutputJWTTokenScheme:
    user = await UserRepository(session).get(data.username)

    if user is None:
        return HTTPException(status_code=401, detail="Invalid username")
    elif not check_password(data.password, user.password_hash):
        return HTTPException(status_code=401, detail="Invalid password")

    access_token = await get_jwt(  # TODO: anyway make with this
        user.username, settings.JWT_ACCESS_KEY, settings.JWT_ACCESS_TOKEN_EXPIRE
    )
    refresh_token = await get_jwt(
        user.username, settings.JWT_REFRESH_KEY, settings.JWT_REFRESH_TOKEN_EXPIRE
    )

    await set_refresh_coockie(response, refresh_token)

    return OutputJWTTokenScheme(access_token=access_token)


@router_auth.post("/refresh")
async def refresh(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
) -> OutputJWTTokenScheme:
    refresh_token = request.cookies.get(settings.COOCKIE_JWT_REFRESH_KEY)

    if refresh_token is None:
        raise HTTPException(status_code=404, detail="Refresh token not found")

    access, refresh = await update_jwt(access_token, refresh_token, session)
    if access is None or refresh is None:
        raise HTTPException(status_code=401, detail="Expired tokens")

    await set_refresh_coockie(response, refresh)

    return OutputJWTTokenScheme(access_token=access_token)
