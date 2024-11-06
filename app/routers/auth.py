from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from jwt import ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession


from app.dependes import get_async_session
from app.services import (hash_password,
                          check_password,
                          get_jwt,
                          update_jwt)
from app.schemas.auth import LoginRequestSchema, TokenResponseSchema, CreateUserSchema
from app.utils import UsersUtils
from app.settings import settings

router = APIRouter(prefix='/auth', tags=['auth'])
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post('/registration')
async def registration(user: CreateUserSchema,
            session: AsyncSession = Depends(get_async_session)):
    user = await UsersUtils(session).create(
        user.name,
        user.username,
        user.email,
        user.password)
    return user

@router.post('/login')
async def login(response: Response,
                data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: AsyncSession = Depends(get_async_session)):
    user = await UsersUtils(session).get(data.username)
    if user is None:
        return HTTPException(status_code=401, detail="Invalid username")
    if not check_password(data.password, user.password_hash.encode()):
        return HTTPException(status_code=401, detail="Invalid password")

    access_token = await get_jwt(
        user.username,
        settings.JWT_ACCESS_KEY,
        settings.JWT_ACCESS_TOKEN_EXPIRE
        )
    refresh_token = await get_jwt(
        user.username,
        settings.JWT_REFRESH_KEY,
        settings.JWT_REFRESH_TOKEN_EXPIRE
        )

    response.set_cookie(
        key="refresh_token_messenger",
        value=refresh_token,
        httponly=True,
        max_age=settings.JWT_REFRESH_TOKEN_EXPIRE,
        secure=True,
        samesite="lax"
    )


    return {'access_token': access_token, 'token_type': 'bearer'}

@router.post('/refresh')
async def refresh(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_async_session)
    ):
    refresh_token = request.cookies.get("refresh_token_messenger")
    if refresh_token is None:
        raise HTTPException(status_code=404, detail="Refresh token not found")

    access, refresh = await update_jwt(access_token, refresh_token, session)
    if access is None or refresh is None:
        raise HTTPException(status_code=401, detail="Expired tokens")

    response.set_cookie(
        key="refresh_token_messenger",
        value=refresh,
        httponly=True,
        max_age=settings.JWT_REFRESH_TOKEN_EXPIRE,
        secure=True,
        samesite="lax"
    )

    return {"access_token": access, 'token_type': 'bearer'}























# @router.post("/refresh", response_model=TokenResponseSchema)
# async def refresh_token(refresh_token: str = Depends(oauth2_scheme)):
#     try:
#         payload = decode_jwt(refresh_token)
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=401, detail="Invalid refresh token")

#         # Генерация нового access токена
#         access_token = get_access_token_jwt({"sub": username})
#         return TokenResponseSchema(access_token=access_token, refresh_token=refresh_token)
#     except ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Refresh token expired")

# @router.get("/protected")
# async def protected_route(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = decode_jwt(token)
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         return {"message": f"Hello, {username}"}
#     except ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Access token expired")
