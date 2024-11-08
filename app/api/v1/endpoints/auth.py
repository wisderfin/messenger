from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated


from app.core.settings import settings
from app.core.database_session import get_async_session
from app.services.auth import hash_password, check_password
from app.services.auth import get_jwt, update_jwt
from app.services.auth import set_refresh_coockie
from app.schemes.auth import CreateUserScheme, OutputUserScheme
from app.schemes.auth import OutputTokenScheme
from app.repositories.auth import UsersUtils


router_auth = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router_auth.post("/registration")
async def registration(
    user: CreateUserScheme, session: AsyncSession = Depends(get_async_session)
) -> OutputUserScheme:
    # TODO: validate email trought send code
    user_model = await UsersUtils(session).create(
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
) -> OutputTokenScheme:
    user = await UsersUtils(session).get(data.username)

    if user is None:
        return HTTPException(status_code=401, detail="Invalid username")
    elif not check_password(data.password, user.password_hash):
        return HTTPException(status_code=401, detail="Invalid password")

    access_token = await get_jwt(
        user.username, settings.JWT_ACCESS_KEY, settings.JWT_ACCESS_TOKEN_EXPIRE
    )
    refresh_token = await get_jwt(
        user.username, settings.JWT_REFRESH_KEY, settings.JWT_REFRESH_TOKEN_EXPIRE
    )

    await set_refresh_coockie(response, refresh_token)

    return OutputTokenScheme(access_token=access_token)


@router_auth.post("/refresh")
async def refresh(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
) -> OutputTokenScheme:
    refresh_token = request.cookies.get(settings.COOCKIE_JWT_REFRESH_KEY)

    if refresh_token is None:
        raise HTTPException(status_code=404, detail="Refresh token not found")

    access, refresh = await update_jwt(access_token, refresh_token, session)
    if access is None or refresh is None:
        raise HTTPException(status_code=401, detail="Expired tokens")

    await set_refresh_coockie(response, refresh)

    return OutputTokenScheme(access_token=access_token)
