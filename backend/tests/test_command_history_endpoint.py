from datetime import UTC, datetime, timedelta
from uuid import uuid4

import httpx

from app.database.dal import DAL
from app.database.enums import CommandStatus
from app.database.models import Command

T0 = datetime(2026, 1, 1, tzinfo=UTC)


async def test_get_history_returns_entries_latest_first(client: httpx.AsyncClient, command: Command) -> None:
    repo = DAL.command_history()
    await repo.create({"command_id": command.id, "status": CommandStatus.PENDING, "params": "1,2", "created_at": T0})
    await repo.create(
        {"command_id": command.id, "status": CommandStatus.SCHEDULED, "created_at": T0 + timedelta(minutes=1)}
    )

    response = await client.get(f"/api/commands/{command.id}/history")

    assert response.status_code == 200
    data = response.json()["data"]
    assert [entry["status"] for entry in data] == ["scheduled", "pending"]
    assert set(data[0]) == {"id", "command_id", "status", "params", "created_at"}
    assert data[0]["command_id"] == str(command.id)
    assert data[1]["params"] == "1,2"
    assert data[0]["created_at"] > data[1]["created_at"]


async def test_unknown_command_returns_empty_list(client: httpx.AsyncClient) -> None:
    response = await client.get(f"/api/commands/{uuid4()}/history")
    assert response.status_code == 200
    assert response.json()["data"] == []


async def test_invalid_id_is_422(client: httpx.AsyncClient) -> None:
    response = await client.get("/api/commands/not-a-uuid/history")
    assert response.status_code == 422
