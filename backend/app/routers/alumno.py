import os
import uuid
from datetime import datetime, timezone, timedelta
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


def _vacante_light(v: Vacante, alumno_id: int | None = None):
    registradas = (
        sum(1 for s in v.solicitudes if s.estatus != EstatusEnum.cancelado)
        if v.solicitudes else 0
    )
    aceptadas = (
        sum(1 for s in v.solicitudes if s.estatus == EstatusEnum.aceptado)
        if v.solicitudes else 0
    )
    confirmadas = (
        sum(1 for s in v.solicitudes if s.estatus == EstatusEnum.aceptado and s.confirmada_por_alumno)
        if v.solicitudes else 0
    )
    is_closed = v.finalizada or v.cerrada_manualmente or not v.activa or aceptadas >= v.cupo_maximo or confirmadas >= v.cupo_maximo
    if v.finalizada:
        status = "finalizada"
    elif is_closed:
        status = "cerrada"
    else:
        status = "abierta"
    result = {
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
        "finalizada": v.finalizada,
        "solicitudes_count": registradas,
        "solicitudes_aceptadas_count": aceptadas,
        "solicitudes_confirmadas_count": confirmadas,
        "is_closed": is_closed,
        "status": status,
    }
    if alumno_id is not None:
        existing = (
            v.solicitudes
            and next(
                (s for s in v.solicitudes if s.alumno_id == alumno_id), None
            )
        )
        if existing:
            result["ha_aplicado"] = True
            result["status_aplicacion"] = existing.estatus.value
        else:
            result["ha_aplicado"] = False
            result["status_aplicacion"] = None
    return result


def _solicitud_to_dict(s: Solicitud):
    return {
        "id": s.id,
        "vacante_id": s.vacante_id,
        "vacante_titulo": s.vacante.titulo if s.vacante else "",
        "empresa_nombre": s.vacante.empresa_nombre if s.vacante else "",
        "estatus": s.estatus.value,
        "confirmada": s.confirmada_por_alumno,
        "codigo_confirmacion": s.codigo_confirmacion,
        "fecha_limite": s.fecha_limite_respuesta.isoformat() if s.fecha_limite_respuesta else None,
        "respondido_en": s.respondido_en.isoformat() if s.respondido_en else None,
    }


# ---- Dashboard ----
@router.get("/dashboard")
def alumno_dashboard(
    current_user: User = alumno_only, db: Session = Depends(get_db)
):
    expirar_aceptaciones_vencidas(db)
    alumno = _get_alumno(current_user, db)

    all_solicitudes = (
        db.query(Solicitud)
        .filter(Solicitud.alumno_id == alumno.id)
        .order_by(Solicitud.id.desc())
        .all()
    )

    pendientes = [s for s in all_solicitudes if s.estatus == EstatusEnum.pendiente]
    por_confirmar = [s for s in all_solicitudes if s.estatus == EstatusEnum.aceptado and not s.confirmada_por_alumno]
    confirmada = next(
        (s for s in all_solicitudes if s.estatus == EstatusEnum.aceptado and s.confirmada_por_alumno and not s.vacante.finalizada),
        None,
    )
    cancelada = next(
        (s for s in all_solicitudes if s.estatus == EstatusEnum.cancelado),
        None,
    )
    finalizada = next(
        (s for s in all_solicitudes if s.estatus == EstatusEnum.aceptado and s.confirmada_por_alumno and s.vacante and s.vacante.finalizada),
        None,
    )

    servicio_completado = finalizada is not None
    servicio_cancelado = (
        cancelada is not None
        and not servicio_completado
        and not pendientes
        and not por_confirmar
        and all_solicitudes
        and all_solicitudes[0].id == cancelada.id
    )

    # Available vacantes — only shown if no confirmed and not completed
    if servicio_completado or confirmada is not None:
        vacantes_disponibles = []
    else:
        # Get vacantes the alumno already has an active solicitud for (pendiente or aceptado)
        active_vacante_ids = set(
            s.vacante_id for s in all_solicitudes
            if s.estatus in (EstatusEnum.pendiente, EstatusEnum.aceptado)
        )
        query = db.query(Vacante).filter(
            Vacante.activa == True,
            Vacante.cerrada_manualmente == False,
            Vacante.finalizada == False,
        )
        if active_vacante_ids:
            query = query.filter(~Vacante.id.in_(active_vacante_ids))
        open_vacantes = query.order_by(Vacante.id.desc()).all()
        vacantes_disponibles = [_vacante_light(v, alumno.id) for v in open_vacantes]

    return {
        "alumno": {
            "id": alumno.id,
            "nombre": alumno.nombre,
            "matricula": alumno.matricula,
            "carrera": alumno.carrera.nombre if alumno.carrera else None,
        },
        "servicio_completado": servicio_completado,
        "servicio_cancelado": servicio_cancelado,
        "vacantes_disponibles": vacantes_disponibles,
        "mis_postulaciones": {
            "pendientes": [_solicitud_to_dict(s) for s in pendientes],
            "por_confirmar": [_solicitud_to_dict(s) for s in por_confirmar],
            "confirmada": _solicitud_to_dict(confirmada) if confirmada else None,
            "cancelada": _solicitud_to_dict(cancelada) if cancelada else None,
            "finalizada": _solicitud_to_dict(finalizada) if finalizada else None,
            "rechazadas": [_solicitud_to_dict(s) for s in all_solicitudes if s.estatus == EstatusEnum.rechazado],
        },
    }


# ---- Mis postulaciones (replaces catalog) ----
@router.get("/vacantes")
def list_mis_postulaciones(
    current_user: User = alumno_only, db: Session = Depends(get_db)
):
    expirar_aceptaciones_vencidas(db)
    alumno = _get_alumno(current_user, db)
    all_solicitudes = (
        db.query(Solicitud)
        .filter(Solicitud.alumno_id == alumno.id)
        .order_by(Solicitud.id.desc())
        .all()
    )

    pendientes = [s for s in all_solicitudes if s.estatus == EstatusEnum.pendiente]
    por_confirmar = [s for s in all_solicitudes if s.estatus == EstatusEnum.aceptado and not s.confirmada_por_alumno]
    confirmada = next(
        (s for s in all_solicitudes if s.estatus == EstatusEnum.aceptado and s.confirmada_por_alumno and not (s.vacante and s.vacante.finalizada)),
        None,
    )
    cancelada = next(
        (s for s in all_solicitudes if s.estatus == EstatusEnum.cancelado),
        None,
    )

    rechazadas = [s for s in all_solicitudes if s.estatus == EstatusEnum.rechazado]

    return {
        "pendientes": [_solicitud_to_dict(s) for s in pendientes],
        "por_confirmar": [_solicitud_to_dict(s) for s in por_confirmar],
        "confirmada": _solicitud_to_dict(confirmada) if confirmada else None,
        "cancelada": _solicitud_to_dict(cancelada) if cancelada else None,
        "rechazadas": [_solicitud_to_dict(s) for s in rechazadas],
    }


@router.get("/vacantes/{id}")
def get_vacante(
    id: int,
    current_user: User = alumno_only,
    db: Session = Depends(get_db),
):
    alumno = _get_alumno(current_user, db)
    v = db.query(Vacante).filter(Vacante.id == id).first()
    if not v:
        raise HTTPException(status_code=404)
    return _vacante_light(v, alumno.id)


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

    # Check if there's already a pendiente or aceptado solicitud for this vacante
    existing = (
        db.query(Solicitud)
        .filter(
            Solicitud.alumno_id == alumno.id,
            Solicitud.vacante_id == vacante.id,
        )
        .first()
    )
    if existing:
        if existing.estatus in (EstatusEnum.pendiente, EstatusEnum.aceptado):
            raise HTTPException(
                status_code=400,
                detail="Ya has aplicado a esta vacante anteriormente",
            )
        if existing.estatus == EstatusEnum.rechazado:
            rejection_time = existing.respondido_en
            if rejection_time and (datetime.utcnow() - rejection_time).days < 7:
                remaining = 7 - (datetime.utcnow() - rejection_time).days
                raise HTTPException(
                    status_code=400,
                    detail=f"Debes esperar {remaining} día(s) para reaplicar a esta vacante",
                )

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

    # Check if student has a confirmed (not canceled/finalized) solicitud
    already_confirmed = (
        db.query(Solicitud)
        .join(Vacante)
        .filter(
            Solicitud.alumno_id == alumno.id,
            Solicitud.estatus == EstatusEnum.aceptado,
            Solicitud.confirmada_por_alumno == True,
        )
        .first()
    )
    if already_confirmed:
        if already_confirmed.vacante and already_confirmed.vacante.finalizada:
            raise HTTPException(
                status_code=400, detail="Ya completaste tu servicio social"
            )
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

    # Cancel other pending acceptances
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

    # Cancel other pending applications
    db.query(Solicitud).filter(
        Solicitud.alumno_id == alumno.id,
        Solicitud.id != solicitud.id,
        Solicitud.estatus == EstatusEnum.pendiente,
    ).update(
        {
            Solicitud.estatus: EstatusEnum.rechazado,
            Solicitud.respondido_en: datetime.now(timezone.utc),
        }
    )
    db.commit()

    return {"mensaje": "Vacante confirmada correctamente"}
