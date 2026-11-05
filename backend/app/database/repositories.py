from uuid import UUID

from sqlmodel import select

from app.database.abstract_repository import AbstractRepository
from app.database.engine import get_db_session
from app.database.models import Command, CommandHistory, MainCommand


class MainCommandRepository(AbstractRepository[MainCommand, int]):
    """
    Repository for MainCommand table.
    """

    model = MainCommand


class CommandsRepository(AbstractRepository[Command, UUID]):
    """
    Repository for Command table.
    """

    model = Command


class CommandHistoryRepository(AbstractRepository[CommandHistory, UUID]):
    """
    Repository for Command table.
    """

    model = CommandHistory

    async def get_history_by_id(self, command_id: UUID) -> list[CommandHistory]:
        """
        Get the entire history of a command by its UUID, sorted by latest first.
        """
        # TODO: Implemented
        async with get_db_session() as session:
            return list(
                (
                    await session.exec(
                        select(CommandHistory)
                        .where(CommandHistory.command_id == command_id)
                        .order_by(CommandHistory.created_at.desc())
                    )
                ).all()
            )
