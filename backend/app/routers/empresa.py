import os
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.empresa import Empresa
from app.models.vacante import Vacante
from app.models.solicitud import Solicitud, EstatusEnum
from app.schemas.vacante import VacanteCreate, VacanteUpdate
from app.middleware import require_role
from app.metrics import vacantes_llenas_total
from app.services.solicitud_service import (
    expirar_aceptaciones_vencidas,
    fecha_limite_nueva,
)

router = APIRouter(prefix="/api/empresa", tags=["empresa"])
empresa_only = Depends(require_role("empresa"))

UPLOAD_BASE = "/app/uploads"


def _get_empresa(current_user: User, db: Session) -> Empresa:
    emp = db.query(Empresa).filter(Empresa.user_id == current_user.id).first()
    if not emp:
        raise HTTPException(status_code=403, detail="Perfil de empresa no encontrado")
    return emp


def _vacante_to_dict(v: Vacante):
    registradas = (
        sum(1 for s in v.solicitudes if s.estatus != EstatusEnum.cancelado)
        if v.solicitudes else 0
    )
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
    is_closed = (
        v.finalizada
        or v.cerrada_manualmente
        or not v.activa
        or aceptadas >= v.cupo_maximo
        or confirmadas >= v.cupo_maximo
    )
    if v.finalizada:
        status = "finalizada"
    elif is_closed:
        status = "cerrada"
    else:
        status = "abierta"
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
        "finalizada": v.finalizada,
        "solicitudes_count": registradas,
        "solicitudes_aceptadas_count": aceptadas,
        "solicitudes_confirmadas_count": confirmadas,
        "is_closed": is_closed,
        "status": status,
    }


# ---- Dashboard ----
@router.get("/dashboard")
def empresa_dashboard(
    current_user: User = empresa_only, db: Session = Depends(get_db)
):
    expirar_aceptaciones_vencidas(db)
    emp = _get_empresa(current_user, db)
    vacantes = db.query(Vacante).filter(Vacante.empresa_id == emp.id).all()

    vacantes_abiertas = 0
    for v in vacantes:
        if v.finalizada or not v.activa or v.cerrada_manualmente:
            continue
        aceptadas = (
            sum(1 for s in v.solicitudes if s.estatus == EstatusEnum.aceptado)
            if v.solicitudes else 0
        )
        confirmadas = (
            sum(1 for s in v.solicitudes if s.estatus == EstatusEnum.aceptado and s.confirmada_por_alumno)
            if v.solicitudes else 0
        )
        if aceptadas < v.cupo_maximo and confirmadas < v.cupo_maximo:
            vacantes_abiertas += 1

    postulantes_activos = (
        db.query(Solicitud)
        .join(Vacante)
        .filter(
            Vacante.empresa_id == emp.id,
            Vacante.finalizada == False,
            Solicitud.estatus.in_([EstatusEnum.pendiente, EstatusEnum.aceptado]),
        )
        .count()
    )

    return {
        "vacantes": len(vacantes),
        "abiertas": vacantes_abiertas,
        "postulantes": postulantes_activos,
        "vacantes_lista": [_vacante_to_dict(v) for v in vacantes[-5:]],
    }


# ---- Vacantes CRUD ----
@router.get("/vacantes")
def list_vacantes(
    current_user: User = empresa_only, db: Session = Depends(get_db)
):
    expirar_aceptaciones_vencidas(db)
    emp = _get_empresa(current_user, db)
    vacantes = (
        db.query(Vacante)
        .filter(Vacante.empresa_id == emp.id)
        .order_by(Vacante.id.desc())
        .all()
    )
    return [_vacante_to_dict(v) for v in vacantes]


@router.post("/vacantes", status_code=201)
def create_vacante(
    data: VacanteCreate,
    current_user: User = empresa_only,
    db: Session = Depends(get_db),
):
    emp = _get_empresa(current_user, db)
    v = Vacante(
        empresa_id=emp.id,
        empresa_nombre=emp.nombre,
        titulo=data.titulo,
        descripcion=data.descripcion,
        requisitos=data.requisitos,
        horario=data.horario,
        ubicacion=data.ubicacion,
        cupo_maximo=data.cupo_maximo,
        limite_registros=data.limite_registros,
    )
    db.add(v)
    db.commit()
    db.refresh(v)
    return _vacante_to_dict(v)


@router.put("/vacantes/{id}")
def update_vacante(
    id: int,
    data: VacanteUpdate,
    current_user: User = empresa_only,
    db: Session = Depends(get_db),
):
    emp = _get_empresa(current_user, db)
    v = (
        db.query(Vacante)
        .filter(Vacante.id == id, Vacante.empresa_id == emp.id)
        .first()
    )
    if not v:
        raise HTTPException(status_code=404)
    v.titulo = data.titulo
    v.descripcion = data.descripcion
    v.requisitos = data.requisitos
    v.horario = data.horario
    v.ubicacion = data.ubicacion
    v.cupo_maximo = data.cupo_maximo
    v.limite_registros = data.limite_registros
    db.commit()
    db.refresh(v)
    return _vacante_to_dict(v)


@router.delete("/vacantes/{id}", status_code=204)
def delete_vacante(
    id: int,
    current_user: User = empresa_only,
    db: Session = Depends(get_db),
):
    emp = _get_empresa(current_user, db)
    v = (
        db.query(Vacante)
        .filter(Vacante.id == id, Vacante.empresa_id == emp.id)
        .first()
    )
    if not v:
        raise HTTPException(status_code=404)
    db.delete(v)
    db.commit()


# ---- Toggle open/close ----
@router.post("/vacantes/{id}/toggle")
def toggle_vacante(
    id: int,
    current_user: User = empresa_only,
    db: Session = Depends(get_db),
):
    emp = _get_empresa(current_user, db)
    v = (
        db.query(Vacante)
        .filter(Vacante.id == id, Vacante.empresa_id == emp.id)
        .first()
    )
    if not v:
        raise HTTPException(status_code=404)
    v.activa = v.cerrada_manualmente or not v.activa
    v.cerrada_manualmente = not v.cerrada_manualmente
    db.commit()
    db.refresh(v)
    return _vacante_to_dict(v)


@router.post("/vacantes/{id}/finalizar")
def finalizar_vacante(
    id: int,
    current_user: User = empresa_only,
    db: Session = Depends(get_db),
):
    emp = _get_empresa(current_user, db)
    v = (
        db.query(Vacante)
        .filter(Vacante.id == id, Vacante.empresa_id == emp.id)
        .first()
    )
    if not v:
        raise HTTPException(status_code=404)
    v.finalizada = True
    v.activa = False
    db.commit()
    db.refresh(v)
    return _vacante_to_dict(v)


# ---- Postulantes ----
@router.get("/vacantes/{id}/postulantes")
def list_postulantes(
    id: int,
    current_user: User = empresa_only,
    db: Session = Depends(get_db),
):
    emp = _get_empresa(current_user, db)
    v = (
        db.query(Vacante)
        .filter(Vacante.id == id, Vacante.empresa_id == emp.id)
        .first()
    )
    if not v:
        raise HTTPException(status_code=404)
    solicitudes = (
        db.query(Solicitud).filter(Solicitud.vacante_id == v.id).all()
    )
    return [
        {
            "id": s.id,
            "alumno_nombre": s.alumno.nombre if s.alumno else "N/A",
            "alumno_matricula": s.alumno.matricula if s.alumno else "N/A",
            "alumno_carrera": s.alumno.carrera.nombre if s.alumno and s.alumno.carrera else "",
            "estatus": s.estatus.value,
            "confirmada": s.confirmada_por_alumno,
            "fecha_limite": s.fecha_limite_respuesta.isoformat()
            if s.fecha_limite_respuesta
            else None,
            "tiene_cv": bool(s.cv),
            "tiene_carta": bool(s.carta),
            "tiene_historial": bool(s.historial),
        }
        for s in solicitudes
    ]


# ---- Accept / Reject ----
@router.post("/solicitudes/{id}/aceptar")
def aceptar_solicitud(
    id: int,
    current_user: User = empresa_only,
    db: Session = Depends(get_db),
):
    expirar_aceptaciones_vencidas(db)
    emp = _get_empresa(current_user, db)
    solicitud = (
        db.query(Solicitud)
        .join(Vacante)
        .filter(
            Solicitud.id == id,
            Vacante.empresa_id == emp.id,
        )
        .first()
    )
    if not solicitud:
        raise HTTPException(status_code=404)
    vacante = solicitud.vacante

    aceptadas = (
        db.query(Solicitud)
        .filter(
            Solicitud.vacante_id == vacante.id,
            Solicitud.estatus == EstatusEnum.aceptado,
        )
        .count()
    )
    if (
        vacante.cerrada_manualmente
        or not vacante.activa
        or aceptadas >= vacante.cupo_maximo
    ):
        raise HTTPException(
            status_code=400, detail="Vacante cerrada o cupo alcanzado"
        )

    alumno_confirmado = (
        db.query(Solicitud)
        .filter(
            Solicitud.alumno_id == solicitud.alumno_id,
            Solicitud.estatus == EstatusEnum.aceptado,
            Solicitud.confirmada_por_alumno == True,
            Solicitud.id != solicitud.id,
        )
        .first()
    )
    if alumno_confirmado:
        raise HTTPException(
            status_code=400,
            detail="El alumno ya confirmó otra vacante",
        )

    solicitud.estatus = EstatusEnum.aceptado
    solicitud.confirmada_por_alumno = False
    solicitud.fecha_limite_respuesta = fecha_limite_nueva()
    solicitud.respondido_en = None
    db.commit()

    if aceptadas + 1 >= vacante.cupo_maximo:
        vacantes_llenas_total.inc()

    return {"mensaje": "Alumno aceptado. Tiene 48h para confirmar."}


@router.post("/solicitudes/{id}/rechazar")
def rechazar_solicitud(
    id: int,
    current_user: User = empresa_only,
    db: Session = Depends(get_db),
):
    emp = _get_empresa(current_user, db)
    solicitud = (
        db.query(Solicitud)
        .join(Vacante)
        .filter(
            Solicitud.id == id,
            Vacante.empresa_id == emp.id,
        )
        .first()
    )
    if not solicitud:
        raise HTTPException(status_code=404)
    solicitud.estatus = EstatusEnum.rechazado
    solicitud.respondido_en = datetime.now(timezone.utc)
    db.commit()
    return {"mensaje": "Solicitud rechazada"}


@router.post("/solicitudes/{id}/cancelar")
def cancelar_solicitud(
    id: int,
    current_user: User = empresa_only,
    db: Session = Depends(get_db),
):
    emp = _get_empresa(current_user, db)
    solicitud = (
        db.query(Solicitud)
        .join(Vacante)
        .filter(
            Solicitud.id == id,
            Vacante.empresa_id == emp.id,
        )
        .first()
    )
    if not solicitud:
        raise HTTPException(status_code=404)
    if solicitud.estatus != EstatusEnum.aceptado or not solicitud.confirmada_por_alumno:
        raise HTTPException(
            status_code=400,
            detail="Solo se pueden cancelar postulaciones confirmadas",
        )
    solicitud.estatus = EstatusEnum.cancelado
    solicitud.respondido_en = datetime.now(timezone.utc)
    db.commit()
    return {"mensaje": "Servicio social cancelado"}


# ---- PDF document download ----
@router.get("/solicitudes/{id}/documentos/{doc}")
def get_documento(
    id: int,
    doc: str,
    current_user: User = empresa_only,
    db: Session = Depends(get_db),
):
    if doc not in ("cv", "carta", "historial"):
        raise HTTPException(status_code=404)
    emp = _get_empresa(current_user, db)
    solicitud = (
        db.query(Solicitud)
        .join(Vacante)
        .filter(
            Solicitud.id == id,
            Vacante.empresa_id == emp.id,
        )
        .first()
    )
    if not solicitud:
        raise HTTPException(status_code=404)

    ruta = getattr(solicitud, doc, None)
    if not ruta:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    full_path = os.path.join(UPLOAD_BASE, ruta)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado en disco")

    return FileResponse(
        full_path,
        media_type="application/pdf",
        headers={"Content-Disposition": f'inline; filename="{os.path.basename(ruta)}"'},
    )
