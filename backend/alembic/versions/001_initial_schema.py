"""initial schema

Revision ID: 001
Create Date: 2026-05-23
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "carreras",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("clave", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("clave"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("email_verified_at", sa.DateTime(), nullable=True),
        sa.Column("remember_token", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "alumnos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("carrera_id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(255), nullable=False),
        sa.Column("ap_pat", sa.String(255), nullable=False),
        sa.Column("ap_mat", sa.String(255), nullable=False),
        sa.Column("matricula", sa.String(20), nullable=False),
        sa.Column("telefono", sa.String(15), nullable=True),
        sa.Column("semestre", sa.Integer(), nullable=True),
        sa.Column("promedio", sa.Numeric(4, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["carrera_id"], ["carreras.id"], ondelete="RESTRICT"),
    )
    op.create_table(
        "empresas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(255), nullable=False),
        sa.Column("rfc", sa.String(20), nullable=False),
        sa.Column("sector", sa.String(150), nullable=False),
        sa.Column("telefono", sa.String(20), nullable=False),
        sa.Column("direccion", sa.String(255), nullable=False),
        sa.Column("contacto_nombre", sa.String(255), nullable=False),
        sa.Column("contacto_email", sa.String(255), nullable=False),
        sa.Column("activa", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
        sa.UniqueConstraint("rfc"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_table(
        "vacantes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=True),
        sa.Column("empresa_nombre", sa.String(255), nullable=False),
        sa.Column("titulo", sa.String(255), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=False),
        sa.Column("requisitos", sa.Text(), nullable=False),
        sa.Column("horario", sa.String(100), nullable=False),
        sa.Column("ubicacion", sa.String(255), nullable=False),
        sa.Column("cupo_maximo", sa.Integer(), nullable=False),
        sa.Column("limite_registros", sa.Integer(), nullable=False),
        sa.Column("activa", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("cerrada_manualmente", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"], ondelete="SET NULL"),
    )
    op.create_table(
        "solicitudes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("alumno_id", sa.Integer(), nullable=False),
        sa.Column("vacante_id", sa.Integer(), nullable=False),
        sa.Column("estatus", sa.Enum("pendiente", "aceptado", "rechazado", name="estatusenum"), nullable=False, server_default="pendiente"),
        sa.Column("codigo_confirmacion", sa.String(12), nullable=False),
        sa.Column("confirmada_por_alumno", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("fecha_limite_respuesta", sa.DateTime(), nullable=True),
        sa.Column("respondido_en", sa.DateTime(), nullable=True),
        sa.Column("cv", sa.String(255), nullable=False),
        sa.Column("carta", sa.String(255), nullable=False),
        sa.Column("historial", sa.String(255), nullable=False),
        sa.Column("comentario_empresa", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("codigo_confirmacion"),
        sa.ForeignKeyConstraint(["alumno_id"], ["alumnos.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["vacante_id"], ["vacantes.id"], ondelete="CASCADE"),
    )
    op.create_table(
        "sessions",
        sa.Column("id", sa.String(255), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("payload", sa.Text(), nullable=False),
        sa.Column("last_activity", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "password_reset_tokens",
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("token", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("solicitudes")
    op.drop_table("vacantes")
    op.drop_table("empresas")
    op.drop_table("alumnos")
    op.drop_table("carreras")
    op.drop_table("users")
    op.drop_table("sessions")
    op.drop_table("password_reset_tokens")
    sa.Enum(name="estatusenum").drop(op.get_bind(), checkfirst=True)
