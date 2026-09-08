from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from app.api.schemas.responses import MainCommandResponse, MainCommandsResponse
from app.database.dal import DAL
from app.database.repositories import MainCommandRepository

main_commands_router = APIRouter(tags=["MCC", "Main Commands"])

MainCommandRepo = Annotated[MainCommandRepository, Depends(DAL.get_repo(DAL.main_commands))]


@main_commands_router.get("/")
async def get_all_commands(
    main_commands: MainCommandRepo,
) -> MainCommandsResponse:
    """
    Gets the main commands that are available for the MCC

    :param main_commands: injected MainCommand repository.
    :return: the list of all commands.
    """
    items = await main_commands.get_all()
    return MainCommandsResponse(data=items)


@main_commands_router.get("/{command_id}")
async def get_command_by_id(
    command_id: int,
    main_commands: MainCommandRepo,
) -> MainCommandResponse:
    """
    Gets the main command by the id provided

    :param command_id: the ID of the command to retrieve.
    :param main_commands: injected MainCommand repository.
    :return: the matching command.
    """
    try:
        command = await main_commands.get_by_id(command_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Command not found") from e
    return MainCommandResponse(data=command)
