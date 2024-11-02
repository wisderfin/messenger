import asyncio
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from app import settings
from alembic import context
from sqlalchemy.ext.asyncio import AsyncEngine


from app.dependes import Base
from app.models import *


config = context.config

section = config.config_ini_section
config.set_section_option(section, "DB_HOST_FROM", settings.DB_HOST_FROM)
config.set_section_option(section, "DB_PORT", settings.DB_PORT)
config.set_section_option(section, "DB_DATABASE", settings.DB_DATABASE)
config.set_section_option(section, "DB_USER", settings.DB_USER)
config.set_section_option(section, "DB_PASSWORD", settings.DB_PASSWORD)
config.set_section_option(section, "DB_DRIVER", settings.DB_DRIVER)


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
