import os
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.alumno import Alumno
from app.models.vacante import Vacante
from app.models.solicitud import Solicitud, EstatusEnum
from app.schemas.solicitud import SolicitudOut, ConfirmarVacanteRequest
from app.middleware import require_role
from app.services.solicitud_service import (
    expirar_aceptaciones_vencidas,
    generar_codigo,
    fecha_limite_nueva,
)

router = APIRouter(prefix="/api/alumno", tags=["alumno"])
alumno_only = Depends(require_role("alumno"))


def _get_alumno(current_user: User, db: Session) -> Alumno:
    alumno = db.query(Alumno).filter(Alumno.user_id == current_user.id).first()
    if not alumno:
        raise HTTPException(status_code=403, detail="Perfil de alumno no encontrado")
    return alumno


def _vacante_with_counts(v: Vacante):
    registradas = len(v.solicitudes) if v.solicitudes else 0
    aceptadas = (
        sum(1 for s in v.solicitudes if s.estatus == EstatusEnum.aceptado)
        if v.solicitudes
        else 0
    )
    confirmadas = (
        sum(
            1
            for s in v.solicitudes
            if s.estatus == EstatusEnum.aceptado and s.confirmada_por_alumno
        )
        if v.solicitudes
        else 0
    )
    is_closed = v.cerrada_manualmente or not v.activa or registradas >= v.limite_registros or aceptadas >= v.cupo_maximo
    return {
        "id": v.id,
        "empresa_id": v.empresa_id,
        "empresa_nombre": v.empresa_nombre,
        "titulo": v.titulo,
        "descripcion": v.descripcion,
        "requisitos": v.requisitos,
        "horario": v.horario,
        "ubicacion": v.ubicacion,
        "cupo_maximo": v.cupo_maximo,
        "limite_registros": v.limite_registros,
        "activa": v.activa,
        "cerrada_manualmente": v.cerrada_manualmente,
        "solicitudes_count": registradas,
        "solicitudes_aceptadas_count": aceptadas,
        "solicitudes_confirmadas_count": confirmadas,
        "is_closed": is_closed,
    }


# ---- Dashboard ----
@router.get("/dashboard")
def alumno_dashboard(
    current_user: User = alumno_only, db: Session = Depends(get_db)
):
    expirar_aceptaciones_vencidas(db)
    alumno = _get_alumno(current_user, db)
    solicitudes = (
        db.query(Solicitud)
        .filter(Solicitud.alumno_id == alumno.id)
        .order_by(Solicitud.id.desc())
        .all()
    )
    ofertas_pendientes = [
        s
        for s in solicitudes
        if s.estatus == EstatusEnum.aceptado and not s.confirmada_por_alumno
    ]
    confirmadas = [
        s
        for s in solicitudes
        if s.estatus == EstatusEnum.aceptado and s.confirmada_por_alumno
    ]
    pendientes_count = sum(1 for s in solicitudes if s.estatus == EstatusEnum.pendiente)
    rechazadas_count = sum(
        1 for s in solicitudes if s.estatus == EstatusEnum.rechazado
    )
    return {
        "alumno": {
            "id": alumno.id,
            "nombre": alumno.nombre,
            "matricula": alumno.matricula,
            "carrera": alumno.carrera.nombre if alumno.carrera else None,
        },
        "metricas": {
            "solicitudes_enviadas": len(solicitudes),
            "pendientes": pendientes_count,
            "ofertas_pendientes": len(ofertas_pendientes),
            "vacantes_confirmadas": len(confirmadas),
            "rechazadas": rechazadas_count,
        },
        "ofertas_pendientes": [
            {
                "solicitud_id": s.id,
                "vacante_titulo": s.vacante.titulo if s.vacante else "",
                "fecha_limite": s.fecha_limite_respuesta.isoformat()
                if s.fecha_limite_respuesta
                else None,
            }
            for s in ofertas_pendientes
        ],
        "asignaciones_confirmadas": [
            {
                "solicitud_id": s.id,
                "vacante_titulo": s.vacante.titulo if s.vacante else "",
                "empresa": s.vacante.empresa_nombre if s.vacante else "",
            }
            for s in confirmadas
        ],
    }


# ---- Vacantes catalog ----
@router.get("/vacantes")
def list_vacantes(
    current_user: User = alumno_only, db: Session = Depends(get_db)
):
    expirar_aceptaciones_vencidas(db)
    vacantes = (
        db.query(Vacante)
        .filter(Vacante.activa == True, Vacante.cerrada_manualmente == False)
        .order_by(Vacante.id.desc())
        .limit(50)
        .all()
    )
    return [_vacante_with_counts(v) for v in vacantes]


@router.get("/vacantes/{id}")
def get_vacante(
    id: int,
    current_user: User = alumno_only,
    db: Session = Depends(get_db),
):
    v = db.query(Vacante).filter(Vacante.id == id).first()
    if not v:
        raise HTTPException(status_code=404)
    return _vacante_with_counts(v)


# ---- Apply ----
UPLOAD_DIR = "/app/uploads/solicitudes"


@router.post("/solicitudes", response_model=dict, status_code=201)
def apply(
    vacante_id: int = Form(...),
    cv: UploadFile = File(...),
    carta: UploadFile = File(...),
    historial: UploadFile = File(...),
    current_user: User = alumno_only,
    db: Session = Depends(get_db),
):
    expirar_aceptaciones_vencidas(db)
    alumno = _get_alumno(current_user, db)

    vacante = db.query(Vacante).filter(Vacante.id == vacante_id).first()
    if not vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")

    # Check availability
    registradas = (
        db.query(Solicitud).filter(Solicitud.vacante_id == vacante.id).count()
    )
    aceptadas = (
        db.query(Solicitud)
        .filter(
            Solicitud.vacante_id == vacante.id,
            Solicitud.estatus == EstatusEnum.aceptado,
        )
        .count()
    )
    if vacante.cerrada_manualmente or not vacante.activa or registradas >= vacante.limite_registros or aceptadas >= vacante.cupo_maximo:
        raise HTTPException(status_code=400, detail="Vacante no disponible")

    already_confirmed = (
        db.query(Solicitud)
        .filter(
            Solicitud.alumno_id == alumno.id,
            Solicitud.estatus == EstatusEnum.aceptado,
            Solicitud.confirmada_por_alumno == True,
        )
        .first()
    )
    if already_confirmed:
        raise HTTPException(
            status_code=400, detail="Ya confirmaste otra vacante"
        )

    # Validate files
    for f in [cv, carta, historial]:
        if f.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Todos los archivos deben ser PDF")
        content = f.file.read()
        if len(content) > 2 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Archivo excede 2MB")
        f.file.seek(0)

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    def save_file(upload: UploadFile, subdir: str) -> str:
        ext = os.path.splitext(upload.filename)[1] or ".pdf"
        name = f"{uuid.uuid4().hex}{ext}"
        path = os.path.join(UPLOAD_DIR, subdir, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(upload.file.read())
        return f"solicitudes/{subdir}/{name}"

    cv_path = save_file(cv, "cvs")
    carta_path = save_file(carta, "cartas")
    hist_path = save_file(historial, "historiales")
    codigo = generar_codigo(db)

    solicitud = Solicitud(
        alumno_id=alumno.id,
        vacante_id=vacante.id,
        estatus=EstatusEnum.pendiente,
        codigo_confirmacion=codigo,
        cv=cv_path,
        carta=carta_path,
        historial=hist_path,
    )
    db.add(solicitud)
    db.commit()
    db.refresh(solicitud)

    return {
        "mensaje": "Postulación exitosa. Guarda tu código de confirmación.",
        "codigo_confirmacion": codigo,
        "solicitud_id": solicitud.id,
    }


# ---- Confirm vacante ----
@router.post("/solicitudes/{id}/confirmar")
def confirmar(
    id: int,
    data: ConfirmarVacanteRequest,
    current_user: User = alumno_only,
    db: Session = Depends(get_db),
):
    expirar_aceptaciones_vencidas(db)
    alumno = _get_alumno(current_user, db)
    solicitud = (
        db.query(Solicitud)
        .filter(Solicitud.id == id, Solicitud.alumno_id == alumno.id)
        .first()
    )
    if not solicitud:
        raise HTTPException(status_code=404)

    if data.codigo_confirmacion.strip() != solicitud.codigo_confirmacion:
        raise HTTPException(status_code=400, detail="Código incorrecto")

    if solicitud.estatus != EstatusEnum.aceptado or solicitud.confirmada_por_alumno:
        raise HTTPException(status_code=400, detail="Oferta no disponible para confirmar")

    solicitud.confirmada_por_alumno = True
    solicitud.respondido_en = datetime.now(timezone.utc)

    # Reject other pending acceptances
    db.query(Solicitud).filter(
        Solicitud.alumno_id == alumno.id,
        Solicitud.id != solicitud.id,
        Solicitud.estatus == EstatusEnum.aceptado,
        Solicitud.confirmada_por_alumno == False,
    ).update(
        {
            Solicitud.estatus: EstatusEnum.rechazado,
            Solicitud.respondido_en: datetime.now(timezone.utc),
        }
    )
    db.commit()

    return {"mensaje": "Vacante confirmada correctamente"}
