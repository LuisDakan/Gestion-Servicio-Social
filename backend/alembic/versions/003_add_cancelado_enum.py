"""add cancelado to estatusenum

Revision ID: 003
Create Date: 2026-05-24
"""
from typing import Sequence, Union
from alembic import op


revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE estatusenum ADD VALUE 'cancelado'")


def downgrade() -> None:
    op.execute("ALTER TYPE estatusenum RENAME TO estatusenum_old")
    op.execute("CREATE TYPE estatusenum AS ENUM('pendiente', 'aceptado', 'rechazado')")
    op.execute("ALTER TABLE solicitudes ALTER COLUMN estatus TYPE estatusenum USING estatus::text::estatusenum")
    op.execute("DROP TYPE estatusenum_old")
