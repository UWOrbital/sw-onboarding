from datetime import UTC, datetime
from typing import Final
from uuid import UUID, uuid4

from pydantic import model_validator
from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Integer, func
from sqlalchemy.schema import ForeignKey
from sqlmodel import Field, SQLModel

from app.database.enums import CommandStatus

# Schema information
SCHEMA_NAME: Final[str] = "gs"

# Table names in database
MAIN_COMMAND_TABLE_NAME: Final[str] = "main_commands"
COMMANDS_TABLE_NAME: Final[str] = "commands"

MainTableID = int
MainTableIDDatabase = Integer


class MainCommand(SQLModel, table=True):
    """
    Main command model.
    This table represents all the possible commands that can be issued.
    """

    id: MainTableID = Field(primary_key=True, index=True)
    name: str
    params: str | None = None  # None if no params needed
    format: str | None = None  # None if no format needed
    data_size: int = Field(ge=0)
    total_size: int = Field(gt=0)
    priority: int = Field(default=0, ge=0)

    # table information
    __tablename__ = MAIN_COMMAND_TABLE_NAME
    __table_args__ = {"schema": SCHEMA_NAME}

    @model_validator(mode="after")
    def validate_params_format(self) -> "MainCommand":
        """
        Returns self if params and format are both None or have the same number
        of comma-separated values. If one of params or format is missing, or the
        numbers of comma-separated values do not match, raise Exception.
        """
        if (
            self.format is None
            and self.params is None
            or (
                self.params is not None and self.format is not None and self.params.count(",") == self.format.count(",")
            )
        ):
            return self

        if self.params is None:
            raise Exception("Missing params")

        elif self.format is None:
            raise Exception("Missing format")

        else:
            raise Exception("Params and format do not have the same number of values")


class Command(SQLModel, table=True):
    """
    An instance of a MainCommand.
    This table holds the data related to actual commands sent from the ground station up to the OBC.
    """

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    status: CommandStatus = Field(default=CommandStatus.PENDING)
    type_: MainTableID = Column(MainTableIDDatabase, ForeignKey(MainCommand.id))  # type: ignore
    params: str | None = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )

    # table information
    __tablename__ = COMMANDS_TABLE_NAME
    __table_args__ = (
        ForeignKeyConstraint(
            ["type_"],
            [MainCommand.id],  # type: ignore
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        {"schema": SCHEMA_NAME},
    )  # Since the table is in a different schema sqlmodel can't find the table normally
