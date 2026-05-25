from sqlalchemy import String, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Vacante(Base):
    __tablename__ = "vacantes"

    id: Mapped[int] = mapped_column(primary_key=True)
    empresa_id: Mapped[int | None] = mapped_column(
        ForeignKey("empresas.id", ondelete="SET NULL"), nullable=True
    )
    empresa_nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    requisitos: Mapped[str] = mapped_column(Text, nullable=False)
    horario: Mapped[str] = mapped_column(String(100), nullable=False)
    ubicacion: Mapped[str] = mapped_column(String(255), nullable=False)
    cupo_maximo: Mapped[int] = mapped_column(Integer, nullable=False)
    limite_registros: Mapped[int] = mapped_column(Integer, nullable=False)
    activa: Mapped[bool] = mapped_column(Boolean, default=True)
    cerrada_manualmente: Mapped[bool] = mapped_column(Boolean, default=False)
    finalizada: Mapped[bool] = mapped_column(Boolean, default=False)

    empresa = relationship("Empresa", back_populates="vacantes")
    solicitudes = relationship("Solicitud", back_populates="vacante")
