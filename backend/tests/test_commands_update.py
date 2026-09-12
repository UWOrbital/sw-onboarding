from uuid import uuid4

import httpx

from app.database.dal import DAL
from app.database.models import Command


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
