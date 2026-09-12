"""create command_history

Revision ID: 3b7e1c9d2a4f
Revises: f982f0c13497
Create Date: 2026-09-12 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '3b7e1c9d2a4f'
down_revision: Union[str, Sequence[str], None] = 'f982f0c13497'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Kept in sync with app.database.models.SCHEMA_NAME.
SCHEMA_NAME = "gs"

# The ENUM type already exists from the commands table; create_type=False reuses it instead of
# trying to CREATE TYPE again.
command_status = postgresql.ENUM(
    'PENDING', 'SCHEDULED', 'ONGOING', 'CANCELLED', 'FAILED', 'COMPLETED',
    name='commandstatus',
    create_type=False,
)


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('command_history',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('command_id', sa.Uuid(), nullable=False),
    sa.Column('status', command_status, nullable=False),
    sa.Column('params', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema=SCHEMA_NAME
    )
    op.create_index(op.f('ix_gs_command_history_command_id'), 'command_history', ['command_id'], unique=False, schema=SCHEMA_NAME)
    op.create_index(op.f('ix_gs_command_history_id'), 'command_history', ['id'], unique=False, schema=SCHEMA_NAME)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_gs_command_history_id'), table_name='command_history', schema=SCHEMA_NAME)
    op.drop_index(op.f('ix_gs_command_history_command_id'), table_name='command_history', schema=SCHEMA_NAME)
    op.drop_table('command_history', schema=SCHEMA_NAME)
