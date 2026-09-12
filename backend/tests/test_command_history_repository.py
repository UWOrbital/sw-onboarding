from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.database.dal import DAL
from app.database.enums import CommandStatus
from app.database.models import Command, MainCommand

T0 = datetime(2026, 1, 1, tzinfo=UTC)


async def test_history_is_scoped_to_the_command_and_sorted_latest_first(
    command: Command, main_command: MainCommand
) -> None:
    other = await DAL.commands().create({"type_": main_command.id})
    repo = DAL.command_history()
    # Inserted out of chronological order, so the result order can only come from created_at.
    for minutes, status in [(2, CommandStatus.COMPLETED), (0, CommandStatus.PENDING), (1, CommandStatus.SCHEDULED)]:
        await repo.create({"command_id": command.id, "status": status, "created_at": T0 + timedelta(minutes=minutes)})
    await repo.create({"command_id": other.id, "status": CommandStatus.FAILED})

    history = await repo.get_history_by_id(command.id)

    assert [entry.status for entry in history] == [
        CommandStatus.COMPLETED,
        CommandStatus.SCHEDULED,
        CommandStatus.PENDING,
    ]
    assert all(entry.command_id == command.id for entry in history)


async def test_unknown_command_has_empty_history() -> None:
    assert await DAL.command_history().get_history_by_id(uuid4()) == []
