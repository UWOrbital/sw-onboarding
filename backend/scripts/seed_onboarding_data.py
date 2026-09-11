"""
Seeds the PostgreSQL database with the data the onboarding challenge starts from.

Two datasets are written, both idempotently, so the script can be re-run (as ``setup.sh`` does)
without duplicating rows:

- ``gs.main_commands``, read from ``main_commands.csv`` next to this file. Rows are keyed by the ID in the
  CSV, and only the IDs missing from the table are inserted.
- ``gs.commands``, generated at random. The table is topped up to ``RANDOM_COMMAND_COUNT`` rows,
  so an already-seeded database is left alone.

Run from the backend directory, so that the ``app`` package resolves the same way it does for the
application and for alembic::

    cd backend && uv run python -m scripts.seed_onboarding_data
"""

import asyncio
import csv
import random
import string
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Final

from app.database.dal import DAL
from app.database.engine import get_db_engine
from app.database.enums import CommandStatus
from app.database.models import MainCommand

# Source of the main command table. Headerless; the columns are positional, in this order.
MAIN_COMMANDS_CSV: Final[Path] = Path(__file__).resolve().parent / "main_commands.csv"
CSV_COLUMNS: Final[tuple[str, ...]] = ("id", "name", "params", "format", "data_size", "total_size")

# How many rows gs.commands is filled up to, and how far back their timestamps are spread.
RANDOM_COMMAND_COUNT: Final[int] = 50
COMMAND_HISTORY_DAYS: Final[int] = 30

# Weighted so a seeded database looks like one that has been running for a while: mostly finished
# commands, a few still in flight.
STATUS_WEIGHTS: Final[dict[CommandStatus, int]] = {
    CommandStatus.PENDING: 3,
    CommandStatus.SCHEDULED: 2,
    CommandStatus.ONGOING: 1,
    CommandStatus.CANCELLED: 1,
    CommandStatus.FAILED: 2,
    CommandStatus.COMPLETED: 6,
}

# Inclusive bounds used when generating a value for an integer type in a main command's format.
INT_RANGES: Final[dict[str, tuple[int, int]]] = {
    "int16": (-32768, 32767),
    "uint8": (0, 255),
    "int32": (-(2**31), 2**31 - 1),
    "int": (0, 1000),
}
LOG_LEVELS: Final[tuple[str, ...]] = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def read_main_commands() -> list[dict[str, Any]]:
    """
    Parse ``main_commands.csv`` into rows ready to hand to the MainCommand repository.

    Blank lines are skipped and empty cells become None, so a command with no parameters keeps
    both ``params`` and ``format`` unset (which is what MainCommand's validator expects). Whitespace
    inside a cell is collapsed, since the source table wraps long parameter lists across lines.

    :return: one dict of MainCommand field values per CSV row.
    """
    rows: list[dict[str, Any]] = []

    with MAIN_COMMANDS_CSV.open(newline="", encoding="utf-8") as csv_file:
        for line_number, raw_row in enumerate(csv.reader(csv_file), start=1):
            if not any(cell.strip() for cell in raw_row):
                continue

            if len(raw_row) != len(CSV_COLUMNS):
                raise ValueError(
                    f"{MAIN_COMMANDS_CSV.name} line {line_number}: expected {len(CSV_COLUMNS)} columns "
                    f"{CSV_COLUMNS}, got {len(raw_row)}"
                )

            id_, name, params, format_, data_size, total_size = (" ".join(cell.split()) for cell in raw_row)
            rows.append(
                {
                    "id": int(id_),
                    "name": name,
                    "params": params or None,
                    "format": format_ or None,
                    "data_size": int(data_size),
                    "total_size": int(total_size),
                }
            )

    return rows


def random_value(type_name: str) -> str:
    """
    Generate one plausible parameter value for a single type in a main command's format string.

    :param type_name: one comma-separated entry of a MainCommand format, e.g. "float" or "varchar(6)".
    :return: the generated value, rendered as a string.
    """
    name = type_name.strip().lower()

    if name.startswith("varchar"):
        length = int(name[name.index("(") + 1 : name.index(")")])
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

    if name == "datetime":
        offset = timedelta(minutes=random.randint(0, COMMAND_HISTORY_DAYS * 24 * 60))
        return (datetime.now(UTC) + offset).isoformat(timespec="seconds")

    if name in {"float", "double"}:
        return f"{random.uniform(-180.0, 180.0):.4f}"

    if name == "enum":
        return random.choice(LOG_LEVELS)

    low, high = INT_RANGES.get(name, INT_RANGES["int"])
    return str(random.randint(low, high))


def random_params(main_command: MainCommand) -> str | None:
    """
    Generate a parameter string matching a main command's declared format.

    :param main_command: the command type the generated params belong to.
    :return: the serialized params, or None for a command that takes no parameters.
    """
    if main_command.format is None:
        return None
    return ", ".join(random_value(type_name) for type_name in main_command.format.split(","))


async def seed_main_commands() -> tuple[list[MainCommand], int]:
    """
    Insert every CSV row whose ID is not already in ``gs.main_commands``.

    :return: all main commands in the table afterwards, and how many of them this run inserted.
    """
    repository = DAL.main_commands()
    existing = await repository.get_all()
    existing_ids = {main_command.id for main_command in existing}

    inserted = [await repository.create(row) for row in read_main_commands() if row["id"] not in existing_ids]

    return existing + inserted, len(inserted)


async def seed_commands(main_commands: list[MainCommand]) -> int:
    """
    Top ``gs.commands`` up to RANDOM_COMMAND_COUNT rows of randomly generated commands.

    Each generated command points at a random main command, carries params matching that command's
    format, and is backdated to a random point within the last COMMAND_HISTORY_DAYS days.

    :param main_commands: the command types to draw from; must be non-empty.
    :return: how many commands this run inserted.
    """
    if not main_commands:
        raise ValueError("No main commands to generate commands from.")

    repository = DAL.commands()
    missing = RANDOM_COMMAND_COUNT - len(await repository.get_all())
    statuses = list(STATUS_WEIGHTS)
    weights = list(STATUS_WEIGHTS.values())

    for _ in range(max(missing, 0)):
        main_command = random.choice(main_commands)
        await repository.create(
            {
                "type_": main_command.id,
                "params": random_params(main_command),
                "status": random.choices(statuses, weights=weights)[0],
                "created_at": datetime.now(UTC) - timedelta(minutes=random.randint(0, COMMAND_HISTORY_DAYS * 24 * 60)),
            }
        )

    return max(missing, 0)


async def seed() -> None:
    """
    Seed both tables and report what was written.
    """
    main_commands, main_commands_inserted = await seed_main_commands()
    print(f"Main commands: inserted {main_commands_inserted}, {len(main_commands)} total.")

    commands_inserted = await seed_commands(main_commands)
    print(f"Commands: inserted {commands_inserted}, {RANDOM_COMMAND_COUNT} total.")

    await get_db_engine().dispose()


def main() -> None:
    """
    This script seeds data into the PostgreSQL database for onboarding purposes.
    """
    asyncio.run(seed())
    print("Seeded onboarding data.")


if __name__ == "__main__":
    main()
