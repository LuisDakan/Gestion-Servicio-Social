from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    rfc: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    sector: Mapped[str] = mapped_column(String(150), nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)
    direccion: Mapped[str] = mapped_column(String(255), nullable=False)
    contacto_nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    contacto_email: Mapped[str] = mapped_column(String(255), nullable=False)
    activa: Mapped[bool] = mapped_column(Boolean, default=True)

    user = relationship("User", back_populates="empresa")
    vacantes = relationship("Vacante", back_populates="empresa")
