from pydantic import BaseModel
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
