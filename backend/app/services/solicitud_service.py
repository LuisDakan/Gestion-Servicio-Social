import secrets
import string
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.models.solicitud import Solicitud, EstatusEnum
from app.models.vacante import Vacante


HORAS_LIMITE = 48


def generar_codigo(session: Session) -> str:
    chars = string.ascii_uppercase + string.digits
    while True:
        codigo = "".join(secrets.choice(chars) for _ in range(8))
        if not session.query(Solicitud).filter(
            Solicitud.codigo_confirmacion == codigo
        ).first():
            return codigo


def expirar_aceptaciones_vencidas(session: Session) -> int:
    ahora = datetime.now(timezone.utc)
    vencidas = (
        session.query(Solicitud)
        .filter(
            Solicitud.estatus == EstatusEnum.aceptado,
            Solicitud.confirmada_por_alumno == False,
            Solicitud.fecha_limite_respuesta <= ahora,
        )
        .all()
    )
    count = 0
    for s in vencidas:
        s.estatus = EstatusEnum.rechazado
        s.respondido_en = ahora
        count += 1
    if count:
        session.commit()
    return count


def fecha_limite_nueva() -> datetime:
    return datetime.now(timezone.utc) + timedelta(hours=HORAS_LIMITE)
