"""create sessions and commands

This is the schema. You must write SQLModel classes in app/data/models.py that match it exactly.

Revision ID: 0001
Revises:
Create Date: 2026-08-09

"""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS transactional")

    op.create_table(
        "sessions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        schema="transactional",
    )

    op.create_table(
        "commands",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("session_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("type_", sa.Integer(), nullable=False),
        sa.Column("params", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("response", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["transactional.sessions.id"],
            ondelete="CASCADE",
        ),
        schema="transactional",
    )
