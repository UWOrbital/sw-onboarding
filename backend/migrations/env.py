import asyncio
from logging.config import fileConfig
from typing import Any

from sqlalchemy import Connection, pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel

from alembic import context
from app.config.env_settings.backend_config import settings
from app.database import models  # noqa: F401  registers the tables on SQLModel.metadata

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Model's MetaData object, for 'autogenerate' support. Importing app.database.models
# above is what populates it, so every table must be reachable from that module.
target_metadata = SQLModel.metadata


def get_url() -> str:
    """
    Returns the database URL for migrations.

    alembic.ini deliberately leaves ``sqlalchemy.url`` unset so the migrations and the
    application read the same GS_DATABASE_* environment variables. The URL is passed
    directly to the engine rather than through ``config.set_main_option`` so that a
    password containing "%" is not mangled by configparser interpolation.

    :return: the async (asyncpg) connection string
    """
    return settings.db.connection_string


def include_name(name: str | None, type_: str, parent_names: dict[str, str | None]) -> bool:
    """
    Restricts autogenerate to the application schema.

    ``include_schemas=True`` is needed to see the tables in the "gs" schema, but it also
    makes Alembic reflect every other schema in the database and propose dropping what it
    finds there. This filter keeps the comparison scoped to our own schema.

    :param name: the name of the object being considered
    :param type_: the kind of object, e.g. "schema" or "table"
    :param parent_names: the names of the object's parents
    :return: True if the object should be considered by autogenerate
    """
    if type_ == "schema":
        return name == models.SCHEMA_NAME
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_name=include_name,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Configures the migration context against a live connection and runs the migrations.

    :param connection: a synchronous connection proxied off the async connection
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        include_name=include_name,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Creates an async engine and runs the migrations through it.

    asyncpg is the only PostgreSQL driver this project depends on, so Alembic drives it
    with ``run_sync`` instead of opening a second, synchronous connection.
    """
    configuration: dict[str, Any] = dict(config.get_section(config.config_ini_section, {}))
    configuration["sqlalchemy.url"] = get_url()

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
