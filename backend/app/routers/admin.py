from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.carrera import Carrera
from app.models.alumno import Alumno
from app.models.empresa import Empresa
from app.models.vacante import Vacante
from app.models.solicitud import Solicitud, EstatusEnum
from app.schemas.carrera import CarreraCreate, CarreraUpdate, CarreraOut
from app.schemas.alumno import AlumnoCreate, AlumnoUpdate, AlumnoOut
from app.schemas.empresa import EmpresaCreate, EmpresaUpdate, EmpresaOut
from app.services.auth_service import hash_password
from app.services.solicitud_service import expirar_aceptaciones_vencidas
from app.middleware import require_role
from app.metrics import users_registered_total

router = APIRouter(prefix="/api/admin", tags=["admin"])
admin_only = Depends(require_role("admin"))


# ---- Dashboard ----
@router.get("/dashboard")
def admin_dashboard(db: Session = Depends(get_db), _=admin_only):
    expirar_aceptaciones_vencidas(db)
    return {
        "metricas": {
            "carreras": db.query(Carrera).count(),
            "alumnos": db.query(Alumno).count(),
            "empresas": db.query(Empresa).count(),
            "solicitudes": db.query(Solicitud).count(),
        },
        "estado_solicitudes": {
            "pendientes": db.query(Solicitud)
            .filter(Solicitud.estatus == EstatusEnum.pendiente)
            .count(),
            "por_confirmar": db.query(Solicitud)
            .filter(
                Solicitud.estatus == EstatusEnum.aceptado,
                Solicitud.confirmada_por_alumno == False,
            )
            .count(),
            "confirmadas": db.query(Solicitud)
            .filter(
                Solicitud.estatus == EstatusEnum.aceptado,
                Solicitud.confirmada_por_alumno == True,
            )
            .count(),
            "rechazadas": db.query(Solicitud)
            .filter(Solicitud.estatus == EstatusEnum.rechazado)
            .count(),
        },
    }


# ---- Carreras CRUD ----
@router.get("/carreras", response_model=list[CarreraOut])
def list_carreras(db: Session = Depends(get_db), _=admin_only):
    return db.query(Carrera).order_by(Carrera.nombre).all()


@router.post("/carreras", response_model=CarreraOut, status_code=201)
def create_carrera(data: CarreraCreate, db: Session = Depends(get_db), _=admin_only):
    exists = (
        db.query(Carrera)
        .filter((Carrera.nombre == data.nombre) | (Carrera.clave == data.clave))
        .first()
    )
    if exists:
        raise HTTPException(status_code=400, detail="Ya existe una carrera con esa clave o nombre")
    c = Carrera(clave=data.clave, nombre=data.nombre)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.put("/carreras/{id}", response_model=CarreraOut)
def update_carrera(
    id: int, data: CarreraUpdate, db: Session = Depends(get_db), _=admin_only
):
    c = db.query(Carrera).filter(Carrera.id == id).first()
    if not c:
        raise HTTPException(status_code=404)
    c.clave = data.clave
    c.nombre = data.nombre
    db.commit()
    db.refresh(c)
    return c


@router.delete("/carreras/{id}", status_code=204)
def delete_carrera(id: int, db: Session = Depends(get_db), _=admin_only):
    c = db.query(Carrera).filter(Carrera.id == id).first()
    if not c:
        raise HTTPException(status_code=404)
    db.delete(c)
    db.commit()


# ---- Alumnos CRUD ----
@router.get("/alumnos", response_model=list[AlumnoOut])
def list_alumnos(db: Session = Depends(get_db), _=admin_only):
    rows = db.query(Alumno).order_by(Alumno.id.desc()).all()
    result = []
    for a in rows:
        out = AlumnoOut.model_validate(a)
        out.carrera_nombre = a.carrera.nombre if a.carrera else None
        result.append(out)
    return result


@router.post("/alumnos", response_model=AlumnoOut, status_code=201)
def create_alumno(data: AlumnoCreate, db: Session = Depends(get_db), _=admin_only):
    username = data.matricula
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="La matrícula ya existe como usuario")
    user = User(
        name=f"{data.nombre} {data.ap_pat} {data.ap_mat}",
        email=f"alumno{username}@serviciosocial.local",
        username=username,
        password=hash_password(username),
        role="alumno",
    )
    db.add(user)
    db.flush()
    alumno = Alumno(
        user_id=user.id,
        carrera_id=data.carrera_id,
        nombre=data.nombre,
        ap_pat=data.ap_pat,
        ap_mat=data.ap_mat,
        matricula=data.matricula,
        telefono=data.telefono,
        semestre=data.semestre,
        promedio=data.promedio,
    )
    db.add(alumno)
    db.commit()
    db.refresh(alumno)
    users_registered_total.labels(role='alumno').inc()
    return AlumnoOut(
        id=alumno.id,
        user_id=alumno.user_id,
        carrera_id=alumno.carrera_id,
        nombre=alumno.nombre,
        ap_pat=alumno.ap_pat,
        ap_mat=alumno.ap_mat,
        matricula=alumno.matricula,
        telefono=alumno.telefono,
        semestre=alumno.semestre,
        promedio=float(alumno.promedio) if alumno.promedio else None,
        carrera_nombre=alumno.carrera.nombre if alumno.carrera else None,
    )


@router.put("/alumnos/{id}", response_model=AlumnoOut)
def update_alumno(
    id: int, data: AlumnoUpdate, db: Session = Depends(get_db), _=admin_only
):
    alumno = db.query(Alumno).filter(Alumno.id == id).first()
    if not alumno:
        raise HTTPException(status_code=404)
    username = data.matricula
    user = db.query(User).filter(User.id == alumno.user_id).first()
    if user:
        user.name = f"{data.nombre} {data.ap_pat} {data.ap_mat}"
        user.email = f"alumno{username}@serviciosocial.local"
        user.username = username
        user.password = hash_password(username)
    for key, val in data.model_dump().items():
        setattr(alumno, key, val)
    db.commit()
    db.refresh(alumno)
    return AlumnoOut(
        id=alumno.id,
        user_id=alumno.user_id,
        carrera_id=alumno.carrera_id,
        nombre=alumno.nombre,
        ap_pat=alumno.ap_pat,
        ap_mat=alumno.ap_mat,
        matricula=alumno.matricula,
        telefono=alumno.telefono,
        semestre=alumno.semestre,
        promedio=float(alumno.promedio) if alumno.promedio else None,
        carrera_nombre=alumno.carrera.nombre if alumno.carrera else None,
    )


@router.delete("/alumnos/{id}", status_code=204)
def delete_alumno(id: int, db: Session = Depends(get_db), _=admin_only):
    alumno = db.query(Alumno).filter(Alumno.id == id).first()
    if not alumno:
        raise HTTPException(status_code=404)
    user_id = alumno.user_id
    db.delete(alumno)
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
    db.commit()


# ---- Empresas CRUD ----
@router.get("/empresas", response_model=list[EmpresaOut])
def list_empresas(db: Session = Depends(get_db), _=admin_only):
    return db.query(Empresa).order_by(Empresa.id.desc()).all()


@router.post("/empresas", response_model=EmpresaOut, status_code=201)
def create_empresa(data: EmpresaCreate, db: Session = Depends(get_db), _=admin_only):
    rfc_up = data.rfc.upper().strip()
    if db.query(User).filter(User.username == rfc_up).first():
        raise HTTPException(status_code=400, detail="RFC ya registrado como usuario")
    if db.query(User).filter(User.email == data.contacto_email).first():
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    user = User(
        name=data.contacto_nombre,
        email=data.contacto_email,
        username=rfc_up,
        password=hash_password(data.password),
        role="empresa",
    )
    db.add(user)
    db.flush()
    emp = Empresa(
        user_id=user.id,
        nombre=data.nombre,
        rfc=rfc_up,
        sector=data.sector,
        telefono=data.telefono,
        direccion=data.direccion,
        contacto_nombre=data.contacto_nombre,
        contacto_email=data.contacto_email,
        activa=data.activa,
    )
    db.add(emp)
    db.commit()
    db.refresh(emp)
    users_registered_total.labels(role='empresa').inc()
    return emp


@router.put("/empresas/{id}", response_model=EmpresaOut)
def update_empresa(
    id: int, data: EmpresaUpdate, db: Session = Depends(get_db), _=admin_only
):
    emp = db.query(Empresa).filter(Empresa.id == id).first()
    if not emp:
        raise HTTPException(status_code=404)
    rfc_up = data.rfc.upper().strip()
    user = db.query(User).filter(User.id == emp.user_id).first()
    if user:
        existing = db.query(User).filter(User.email == data.contacto_email, User.id != user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
        user.name = data.contacto_nombre
        user.email = data.contacto_email
        user.username = rfc_up
        if data.password:
            user.password = hash_password(data.password)
    emp.nombre = data.nombre
    emp.rfc = rfc_up
    emp.sector = data.sector
    emp.telefono = data.telefono
    emp.direccion = data.direccion
    emp.contacto_nombre = data.contacto_nombre
    emp.contacto_email = data.contacto_email
    emp.activa = data.activa
    db.commit()
    db.refresh(emp)
    return emp


@router.delete("/empresas/{id}", status_code=204)
def delete_empresa(id: int, db: Session = Depends(get_db), _=admin_only):
    emp = db.query(Empresa).filter(Empresa.id == id).first()
    if not emp:
        raise HTTPException(status_code=404)
    user_id = emp.user_id
    db.delete(emp)
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
    db.commit()
