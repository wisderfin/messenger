from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing import AsyncGenerator

from settings import settings


engine = create_async_engine(
            f'{settings.DATABASE_DRIVERS}://'
            f'{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}')
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


# генератор сессия базы данных
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
