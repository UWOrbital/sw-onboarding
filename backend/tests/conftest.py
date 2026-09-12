"""
Shared fixtures.

Tests run against a real PostgreSQL database, the one docker-compose starts, but in a separate
database named ``<GS_DATABASE_NAME>_test``. Once per session that database is dropped, recreated,
and migrated to head with alembic, so the migrations are exercised on every run. Every table is
truncated before each test.
"""

import os
import subprocess
import sys
from collections.abc import AsyncIterator
from pathlib import Path

import asyncpg
import httpx
import pytest
from dotenv import load_dotenv
from sqlalchemy import text
from sqlmodel import SQLModel

REPO_ROOT = Path(__file__).resolve().parents[2]

# Same .env the app reads. Variables already in the environment (e.g. in CI) win over the file.
load_dotenv(REPO_ROOT / ".env")
# Must be set before the app's settings singleton is imported.
os.environ["GS_DATABASE_NAME"] = os.environ.get("GS_DATABASE_NAME", "sw_onboarding") + "_test"

from app.config.env_settings.backend_config import settings  # noqa: E402
from app.database.dal import DAL  # noqa: E402
from app.database.engine import get_db_engine  # noqa: E402
from app.database.models import Command, MainCommand  # noqa: E402
from main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
async def database() -> AsyncIterator[None]:
    """Recreate the test database from scratch and migrate it to head, once per session."""
    db = settings.db
    conn = await asyncpg.connect(
        user=db.user,
        password=db.password.get_secret_value(),
        host=db.location,
        port=db.port,
        database="postgres",
    )
    try:
        await conn.execute(f'DROP DATABASE IF EXISTS "{db.name}" WITH (FORCE)')
        await conn.execute(f'CREATE DATABASE "{db.name}"')
    finally:
        await conn.close()

    subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], cwd=REPO_ROOT, check=True)
    yield
    await get_db_engine().dispose()


@pytest.fixture(autouse=True)
async def clean_tables(database: None) -> None:
    """Empty every table the models declare before each test."""
    tables = ", ".join(table.fullname for table in SQLModel.metadata.sorted_tables)
    async with get_db_engine().begin() as conn:
        await conn.execute(text(f"TRUNCATE {tables} CASCADE"))


@pytest.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    """HTTP client wired straight into the FastAPI app, no server needed."""
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.fixture
async def main_command() -> MainCommand:
    """One command type, so commands have something to point at."""
    return await DAL.main_commands().create({"id": 1, "name": "PING", "data_size": 0, "total_size": 1})


@pytest.fixture
async def command(main_command: MainCommand) -> Command:
    """One pending command, inserted directly so it has no history entries."""
    return await DAL.commands().create({"type_": main_command.id, "params": "1,2"})
