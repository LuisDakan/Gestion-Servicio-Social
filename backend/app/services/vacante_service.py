from sqlalchemy.orm import Session

from app.models.vacante import Vacante


def _counts_dict(v: Vacante) -> dict:
    registradas = len(v.solicitudes) if v.solicitudes else 0
    aceptadas = sum(
        1 for s in v.solicitudes if s.estatus == "aceptado"
    ) if v.solicitudes else 0
    confirmadas = sum(
        1 for s in v.solicitudes
        if s.estatus == "aceptado" and s.confirmada_por_alumno
    ) if v.solicitudes else 0
    return dict(
        solicitudes_count=registradas,
        solicitudes_aceptadas_count=aceptadas,
        solicitudes_confirmadas_count=confirmadas,
    )
```

