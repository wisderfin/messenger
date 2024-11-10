import asyncio
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from alembic import context


from app.core.settings import settings
from app.domain.models import *


config = context.config

section = config.config_ini_section
config.set_section_option(section, "DATABASE_HOST", settings.DATABASE_HOST)
config.set_section_option(section, "DATABASE_PORT_FROM", settings.DATABASE_PORT_FROM)
config.set_section_option(section, "DATABASE_NAME", settings.DATABASE_NAME)
config.set_section_option(section, "DATABASE_USER", settings.DATABASE_USER)
config.set_section_option(section, "DATABASE_PASSWORD", settings.DATABASE_PASSWORD)
config.set_section_option(section, "DATABASE_DRIVER", settings.DATABASE_DRIVER)


fileConfig(config.config_file_name)
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
