from datetime import datetime
from typing import cast
from uuid import UUID

from sqlalchemy.sql.elements import ColumnElement  # added for get_history_by_id
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

        # Method should open a database session, select rows from CommandHistory,
        #   filter by command_id, order by created_at descending, and return the list

        # (STEP 1) Implement this stub! (2 tests passed with pytest)
        async with get_db_session() as session:
            statement = (
                select(self.model)
                .where(self.model.command_id == command_id)  # filter
                .order_by(cast(ColumnElement[datetime], CommandHistory.created_at).desc())  # descending order
            )
            # executes SQL query and uses await to pause until query finishes (async)
            results = await session.exec(statement)
            return list(results.all())
