from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    email_verified_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    remember_token: Mapped[str | None] = mapped_column(String(100), nullable=True)

    alumno = relationship("Alumno", back_populates="user", uselist=False)
    empresa = relationship("Empresa", back_populates="user", uselist=False)
