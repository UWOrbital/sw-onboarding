from collections.abc import Iterator
from typing import Any
from uuid import UUID, uuid4

import httpx
import pytest

from app.database.dal import DAL
from app.database.models import Command
from app.database.repositories import CommandsRepository
from main import app


async def test_update_status_only_keeps_other_fields(client: httpx.AsyncClient, command: Command) -> None:
    response = await client.patch(f"/api/commands/{command.id}", json={"status": "scheduled"})

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == str(command.id)
    assert data["status"] == "scheduled"
    assert data["type_"] == command.type_
    assert data["params"] == command.params

    persisted = (await client.get(f"/api/commands/{command.id}")).json()["data"]
    assert persisted["status"] == "scheduled"


async def test_update_type_and_params_keeps_status(client: httpx.AsyncClient, command: Command) -> None:
    other = await DAL.main_commands().create({"id": 2, "name": "OTHER", "data_size": 0, "total_size": 1})

    response = await client.patch(f"/api/commands/{command.id}", json={"type_": other.id, "params": "9"})

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["type_"] == other.id
    assert data["params"] == "9"
    assert data["status"] == "pending"


async def test_update_unknown_command_is_404(client: httpx.AsyncClient) -> None:
    response = await client.patch(f"/api/commands/{uuid4()}", json={"status": "failed"})
    assert response.status_code == 404


async def test_update_invalid_status_is_422(client: httpx.AsyncClient, command: Command) -> None:
    response = await client.patch(f"/api/commands/{command.id}", json={"status": "bogus"})
    assert response.status_code == 422


async def test_update_to_unknown_type_is_422_and_changes_nothing(client: httpx.AsyncClient, command: Command) -> None:
    response = await client.patch(f"/api/commands/{command.id}", json={"type_": 999, "params": "9"})
    assert response.status_code == 422

    persisted = (await client.get(f"/api/commands/{command.id}")).json()["data"]
    assert persisted["type_"] == command.type_
    assert persisted["params"] == command.params


class TypeErrorCommandsRepository(CommandsRepository):
    """Stands in for the real repository when its update rejects a value's type."""

    async def update(self, obj_id: UUID, data: dict[str, Any]) -> Command:
        raise TypeError("Command, field params must be of type str")


@pytest.fixture
def type_error_repo() -> Iterator[None]:
    provider = DAL.get_repo(DAL.commands)
    app.dependency_overrides[provider] = TypeErrorCommandsRepository
    yield
    app.dependency_overrides.pop(provider)


async def test_update_repo_type_error_is_422(
    client: httpx.AsyncClient, command: Command, type_error_repo: None
) -> None:
    response = await client.patch(f"/api/commands/{command.id}", json={"params": "9"})
    assert response.status_code == 422
