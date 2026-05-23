from datetime import datetime
from sqlalchemy import String, Text, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
import enum


class EstatusEnum(str, enum.Enum):
    pendiente = "pendiente"
    aceptado = "aceptado"
    rechazado = "rechazado"


class Solicitud(Base):
    __tablename__ = "solicitudes"

    id: Mapped[int] = mapped_column(primary_key=True)
    alumno_id: Mapped[int] = mapped_column(
        ForeignKey("alumnos.id", ondelete="CASCADE"), nullable=False
    )
    vacante_id: Mapped[int] = mapped_column(
        ForeignKey("vacantes.id", ondelete="CASCADE"), nullable=False
    )
    estatus: Mapped[EstatusEnum] = mapped_column(
        Enum(EstatusEnum), default=EstatusEnum.pendiente, nullable=False
    )
    codigo_confirmacion: Mapped[str] = mapped_column(
        String(12), nullable=False, unique=True
    )
    confirmada_por_alumno: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_limite_respuesta: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    respondido_en: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    cv: Mapped[str] = mapped_column(String(255), nullable=False)
    carta: Mapped[str] = mapped_column(String(255), nullable=False)
    historial: Mapped[str] = mapped_column(String(255), nullable=False)
    comentario_empresa: Mapped[str | None] = mapped_column(Text, nullable=True)

    alumno = relationship("Alumno", back_populates="solicitudes")
    vacante = relationship("Vacante", back_populates="solicitudes")
