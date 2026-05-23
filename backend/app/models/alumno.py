from sqlalchemy import String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Alumno(Base):
    __tablename__ = "alumnos"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    carrera_id: Mapped[int] = mapped_column(
        ForeignKey("carreras.id", ondelete="RESTRICT"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    ap_pat: Mapped[str] = mapped_column(String(255), nullable=False)
    ap_mat: Mapped[str] = mapped_column(String(255), nullable=False)
    matricula: Mapped[str] = mapped_column(String(20), nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(15), nullable=True)
    semestre: Mapped[int | None] = mapped_column(Integer, nullable=True)
    promedio: Mapped[float | None] = mapped_column(Numeric(4, 2), nullable=True)

    user = relationship("User", back_populates="alumno")
    carrera = relationship("Carrera", back_populates="alumnos")
    solicitudes = relationship("Solicitud", back_populates="alumno")
