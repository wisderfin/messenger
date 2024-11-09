from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.models.auth import UserModel
from app.services.auth import hash_password


class UserRepository:  # TODO: arguments for functions is schemes(or may be no, THINKS ABOUT IT)
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, username: str) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).filter_by(username=username)
        )
        user = result.scalar_one_or_none()
        return user

    async def __check(
        self, username: str
    ) -> bool:  # TODO: thinks about a level of private
        user = await self.get(username)
        return user is not None

    async def create(
        self, name: str, username: str, email: str, password: str
    ) -> UserModel | None:
        if await self.__check(username):
            return None  # TODO: HTTP error

        hashed_password = hash_password(password)  # make native (scheme)
        new_user = UserModel(
            name=name, email=email, username=username, password_hash=hashed_password
        )

        self.session.add(new_user)
        try:  # TODO: it's TRASH, corect it and HTTP exeption
            await self.session.commit()
            return new_user
        except IntegrityError:
            await self.session.rollback()
            return None
