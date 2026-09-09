from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from app.database.enums import CommandStatus
from app.database.models import CommandHistory, MainCommand


class CommandHistoryResponse(BaseModel):
    """Response model wrapping a list of CommandHistory objects."""

    data: Annotated[list[CommandHistory], Field(description="A list containing CommandHistory objects")]


class CommandItem(BaseModel):
    """Pydantic response model for a serialized Command (non-table)."""

    model_config = {"from_attributes": True}

    id: UUID
    status: CommandStatus
    type_: int
    params: str | None = None
    created_at: datetime


class CommandsResponse(BaseModel):
    """Response model wrapping a list of Commands."""

    data: Annotated[list[CommandItem], Field(description="A list containing Command objects")]


class CommandResponse(BaseModel):
    """Response model wrapping a single Command."""

    data: Annotated[CommandItem, Field(description="The created or retrieved Command object")]


class DeleteCommandResponse(BaseModel):
    """Response model confirming a command deletion."""

    message: Annotated[str, Field(description="Confirmation message including the deleted command ID")]


class MainCommandsResponse(BaseModel):
    """Response model wrapping a list of MainCommand reference entries."""

    data: Annotated[list[MainCommand], Field(description="A list containing MainCommand objects")]


class MainCommandResponse(BaseModel):
    """Response model wrapping a single MainCommand."""

    data: Annotated[MainCommand, Field(description="The retrieved MainCommand object")]
