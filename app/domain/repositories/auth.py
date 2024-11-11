from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.domain.models.auth import UserModel
from app.domain.services.auth import hash_password


class UserRepository:  # TODO: inheritance from BaseRepository(and make BaseRepository)
    def __init__(
        self, session: AsyncSession
    ) -> None:  # TODO: thinks about generate session in injection class
        self.session = session

    async def get(self, username: str) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).filter_by(username=username)
        )
        user = result.scalar_one_or_none()
        return user

    async def __check(self, username: str) -> bool:
        user = await self.get(username)
        return user is not None

    async def create(
        self, name: str, username: str, email: str, password: str
    ) -> UserModel | None:
        if await self.__check(username):
            raise HTTPException(status_code=409, detail="User already exists")

        hashed_password = hash_password(password)
        new_user = UserModel(
            name=name, email=email, username=username, password_hash=hashed_password
        )

        self.session.add(new_user)
        await self.session.commit()

        return new_user
