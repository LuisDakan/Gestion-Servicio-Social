from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SolicitudOut(BaseModel):
    id: int
    alumno_id: int
    vacante_id: int
    estatus: str
    codigo_confirmacion: Optional[str] = None
    confirmada_por_alumno: bool = False
    fecha_limite_respuesta: Optional[datetime] = None
    respondido_en: Optional[datetime] = None
    cv: str
    carta: str
    historial: str
    comentario_empresa: Optional[str] = None

    class Config:
        from_attributes = True


class ConfirmarVacanteRequest(BaseModel):
    codigo_confirmacion: str
