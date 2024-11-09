from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing import AsyncGenerator

from core import settings


engine = create_async_engine(
    f"{settings.DATABASE_DRIVER}://"
    f"{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@"
    f"{settings.DATABASE_HOST}:{settings.DATABASE_PORT_FROM}/"
    f"{settings.DATABASE_NAME}"
)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


# генератор сессия базы данных
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
