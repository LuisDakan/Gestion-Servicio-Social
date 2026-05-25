from pydantic import BaseModel, field_validator
from typing import Optional


class EmpresaCreate(BaseModel):
    nombre: str
    rfc: str
    sector: str
    telefono: str
    direccion: str
    contacto_nombre: str
    contacto_email: str
    password: str
    activa: bool = True

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v


class EmpresaUpdate(BaseModel):
    nombre: str
    rfc: str
    sector: str
    telefono: str
    direccion: str
    contacto_nombre: str
    contacto_email: str
    password: Optional[str] = None
    activa: bool = True


class EmpresaOut(BaseModel):
    id: int
    user_id: int
    nombre: str
    rfc: str
    sector: str
    telefono: str
    direccion: str
    contacto_nombre: str
    contacto_email: str
    activa: bool

    class Config:
        from_attributes = True
