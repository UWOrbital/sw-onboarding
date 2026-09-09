from collections.abc import Callable
from typing import Any, TypeVar, cast

from app.database.abstract_repository import AbstractRepository
from app.database.repositories import CommandHistoryRepository, CommandsRepository, MainCommandRepository

R = TypeVar("R", bound=AbstractRepository[Any, Any])


class DAL:
    """
    Data Access Layer: the single registry of repositories.

    Each class attribute maps a name to its repository *class*. Two usages:

    - Inside a route, inject the repository via FastAPI's dependency injection::

        commands: Annotated[CommandsRepository, Depends(DAL.get_repo(DAL.commands))]

    - Outside the request lifecycle (services, auth helpers, scripts), instantiate
      the repository directly::

        commands = DAL.commands()
    """

    main_commands = MainCommandRepository
    commands = CommandsRepository
    command_history = CommandHistoryRepository

    # Cache of provider callables keyed by repository class. FastAPI keys
    # dependency_overrides by callable identity, so get_repo must return the
    # *same* provider object for a given repository class to stay overridable.
    _providers: dict[type[Any], Callable[[], Any]] = {}

    @staticmethod
    def get_repo(repo_cls: type[R]) -> Callable[[], R]:
        """
        Return a stable FastAPI dependency provider that instantiates a repository.

        :param repo_cls: the repository class to provide, e.g. ``DAL.commands``.
        :return: a cached zero-argument callable returning a fresh repository instance.
        """
        if repo_cls not in DAL._providers:

            def _provider() -> R:
                return repo_cls()

            DAL._providers[repo_cls] = _provider
        return cast("Callable[[], R]", DAL._providers[repo_cls])
