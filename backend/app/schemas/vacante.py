from pydantic import BaseModel
from typing import Optional


class VacanteCreate(BaseModel):
    titulo: str
    descripcion: str
    requisitos: str
    horario: str
    ubicacion: str
    cupo_maximo: int
    limite_registros: int


class VacanteUpdate(BaseModel):
    titulo: str
    descripcion: str
    requisitos: str
    horario: str
    ubicacion: str
    cupo_maximo: int
    limite_registros: int


class VacanteOut(BaseModel):
    id: int
    empresa_id: Optional[int] = None
    empresa_nombre: str
    titulo: str
    descripcion: str
    requisitos: str
    horario: str
    ubicacion: str
    cupo_maximo: int
    limite_registros: int
    activa: bool
    cerrada_manualmente: bool
    solicitudes_count: int = 0
    solicitudes_aceptadas_count: int = 0
    solicitudes_confirmadas_count: int = 0
    is_closed: bool = False

    class Config:
        from_attributes = True
