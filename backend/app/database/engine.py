from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config.env_settings.backend_config import settings


# the long-lived connection manager to Postgres.
# created once and reused across requests to avoid connection pool exhaustion
@lru_cache(maxsize=1)  # remembers the function's return value for the same arguments, so we only create one engine
def get_db_engine() -> AsyncEngine:
    """
    Creates (once) and returns the async database engine
    Cached so the connection pool is reused across requests

    :return: engine
    """

    # configure the connection pool: a set of ready-to-use database connections shared across requests.
    return create_async_engine(
        settings.db.connection_string,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=1800,
    )


# a short-lived session manager to Postgres.
# opens a new session for each request and closes it after the request is done
def get_db_session() -> AsyncSession:
    """
    Creates a new async session bound to the shared engine

    :return: session
    """
    engine = get_db_engine()
    return AsyncSession(engine, expire_on_commit=False)
