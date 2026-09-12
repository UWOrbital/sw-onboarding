import subprocess
import sys
from datetime import UTC
from pathlib import Path
from uuid import UUID, uuid4

from sqlmodel import SQLModel

from app.database.enums import CommandStatus
from app.database import models
from app.database.models import SCHEMA_NAME, CommandHistory

REPO_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_COLUMNS = {"id", "command_id", "status", "params", "created_at"}


def test_table_is_registered_in_gs_schema() -> None:
    table = CommandHistory.__table__  # type: ignore[attr-defined]
    assert table.schema == SCHEMA_NAME
    assert table.name == models.COMMAND_HISTORY_TABLE_NAME
    assert f"{SCHEMA_NAME}.{models.COMMAND_HISTORY_TABLE_NAME}" in SQLModel.metadata.tables


def test_columns_match_the_command_snapshot() -> None:
    columns = CommandHistory.__table__.columns  # type: ignore[attr-defined]
    assert set(columns.keys()) == EXPECTED_COLUMNS
    assert columns["id"].primary_key
    assert not columns["command_id"].nullable
    assert not columns["status"].nullable
    assert columns["params"].nullable
    assert columns["created_at"].type.timezone
    assert columns["created_at"].server_default is not None


def test_instance_defaults() -> None:
    entry = CommandHistory(command_id=uuid4(), status=CommandStatus.PENDING)
    assert isinstance(entry.id, UUID)
    assert entry.params is None
    assert entry.created_at.tzinfo is UTC


def test_migrations_match_models(database: None) -> None:
    """``alembic check`` fails if autogenerate would emit anything, i.e. if the migration and model differ."""
    subprocess.run([sys.executable, "-m", "alembic", "check"], cwd=REPO_ROOT, check=True)
