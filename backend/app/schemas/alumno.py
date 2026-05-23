from pydantic import BaseModel
from typing import Optional


class AlumnoCreate(BaseModel):
    carrera_id: int
    nombre: str
    ap_pat: str
    ap_mat: str
    matricula: str
    telefono: Optional[str] = None
    semestre: Optional[int] = None
    promedio: Optional[float] = None


class AlumnoUpdate(BaseModel):
    carrera_id: int
    nombre: str
    ap_pat: str
    ap_mat: str
    matricula: str
    telefono: Optional[str] = None
    semestre: Optional[int] = None
    promedio: Optional[float] = None


class AlumnoOut(BaseModel):
    id: int
    user_id: int
    carrera_id: int
    nombre: str
    ap_pat: str
    ap_mat: str
    matricula: str
    telefono: Optional[str] = None
    semestre: Optional[int] = None
    promedio: Optional[float] = None
    carrera_nombre: Optional[str] = None

    class Config:
        from_attributes = True


class AlumnoDashboardOut(BaseModel):
    alumno: "AlumnoOut"
    metricas: dict
    ofertas_pendientes: list
    asignaciones_confirmadas: list
    solicitudes_recientes: list
