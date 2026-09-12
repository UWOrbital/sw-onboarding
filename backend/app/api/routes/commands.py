from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from app.api.routes.command_history import CommandHistoryRepo
from app.api.schemas.requests import CreateCommandRequest, UpdateCommandRequest
from app.api.schemas.responses import CommandResponse, CommandsResponse, DeleteCommandResponse
from app.database.dal import DAL
from app.database.models import Command
from app.database.repositories import CommandHistoryRepository, CommandsRepository

commands_router = APIRouter(tags=["Commands"])

CommandsRepo = Annotated[CommandsRepository, Depends(DAL.get_repo(DAL.commands))]


async def record_history(command_history: CommandHistoryRepository, command: Command) -> None:
    """
    Append the command's current state to its audit log.

    :param command_history: CommandHistory repository to write through.
    :param command: the command whose state is snapshotted.
    """
    await command_history.create(
        {
            "command_id": command.id,
            "status": command.status,
            "params": command.params,
        }
    )


@commands_router.get("/")
async def get_commands(commands: CommandsRepo) -> CommandsResponse:
    """
    Retrieve all commands from the database.

    :param commands: injected Command repository.
    :return: All command entries.
    """
    return CommandsResponse(data=await commands.get_all())


@commands_router.get("/{command_id}")
async def get_command(command_id: UUID, commands: CommandsRepo) -> CommandResponse:
    """
    Retrieve a single command by ID.

    :param command_id: UUID of the command to retrieve.
    :param commands: injected Command repository.
    :return: The matching command entry.
    """
    try:
        command = await commands.get_by_id(command_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return CommandResponse(data=command)


@commands_router.post("/")
async def create_command(
    request: CreateCommandRequest,
    commands: CommandsRepo,
    command_history: CommandHistoryRepo,
) -> CommandResponse:
    """
    Create a new command entry with status set to pending, and record it in the audit log.

    :param request: Typed fields identifying the command type, session, and optional parameters.
    :param commands: injected Command repository.
    :param command_history: injected CommandHistory repository.
    :return: The newly created command.
    """
    created_command = await commands.create(
        {
            "type_": request.type_,
            "params": request.params,
        }
    )
    await record_history(command_history, created_command)
    return CommandResponse(data=created_command)


@commands_router.patch("/{command_id}")
async def update_command(
    command_id: UUID,
    request: UpdateCommandRequest,
    commands: CommandsRepo,
    command_history: CommandHistoryRepo,
) -> CommandResponse:
    """
    Partially update a command's status, type, or parameters, and record the new state in the audit log.

    :param command_id: UUID of the command to update.
    :param request: Fields to overwrite; omitted fields are left unchanged.
    :param commands: injected Command repository.
    :param command_history: injected CommandHistory repository.
    :return: The updated command entry.
    """
    try:
        updated_command = await commands.update(command_id, request.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    await record_history(command_history, updated_command)
    return CommandResponse(data=updated_command)


@commands_router.delete("/{command_id}")
async def delete_command(
    command_id: UUID,
    commands: CommandsRepo,
    command_history: CommandHistoryRepo,
) -> DeleteCommandResponse:
    """
    Delete a command by ID, recording its final state in the audit log first.

    :param command_id: UUID of the command to delete.
    :param commands: injected Command repository.
    :param command_history: injected CommandHistory repository.
    :return: Confirmation message with the deleted command ID.
    """
    try:
        command = await commands.get_by_id(command_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    await record_history(command_history, command)
    await commands.delete_by_id(command_id)
    return DeleteCommandResponse(message=f"Command {command_id} deleted successfully")
