from uuid import UUID

from app.database.abstract_repository import AbstractRepository
from app.database.models import Command, MainCommand


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
