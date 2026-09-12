from uuid import UUID, uuid4

import httpx

from app.database.models import Command, MainCommand


async def history(client: httpx.AsyncClient, command_id: UUID | str) -> list[dict[str, object]]:
    response = await client.get(f"/api/commands/{command_id}/history")
    assert response.status_code == 200
    return response.json()["data"]  # type: ignore[no-any-return]


async def test_create_records_initial_state(client: httpx.AsyncClient, main_command: MainCommand) -> None:
    response = await client.post("/api/commands/", json={"type_": main_command.id, "params": "1,2"})
    assert response.status_code == 200
    command_id = response.json()["data"]["id"]

    entries = await history(client, command_id)

    assert len(entries) == 1
    assert entries[0]["command_id"] == command_id
    assert entries[0]["status"] == "pending"
    assert entries[0]["params"] == "1,2"


async def test_each_update_appends_the_new_state(client: httpx.AsyncClient, command: Command) -> None:
    assert (await client.patch(f"/api/commands/{command.id}", json={"status": "scheduled"})).status_code == 200
    assert (await client.patch(f"/api/commands/{command.id}", json={"params": "3"})).status_code == 200

    entries = await history(client, command.id)

    assert [(e["status"], e["params"]) for e in entries] == [("scheduled", "3"), ("scheduled", command.params)]


async def test_delete_records_final_state_and_keeps_history(client: httpx.AsyncClient, command: Command) -> None:
    assert (await client.patch(f"/api/commands/{command.id}", json={"status": "cancelled"})).status_code == 200

    assert (await client.delete(f"/api/commands/{command.id}")).status_code == 200
    assert (await client.get(f"/api/commands/{command.id}")).status_code == 404

    entries = await history(client, command.id)
    assert [e["status"] for e in entries] == ["cancelled", "cancelled"]
    assert all(e["command_id"] == str(command.id) for e in entries)


async def test_failed_update_records_nothing(client: httpx.AsyncClient) -> None:
    command_id = uuid4()
    assert (await client.patch(f"/api/commands/{command_id}", json={"status": "failed"})).status_code == 404
    assert await history(client, command_id) == []
