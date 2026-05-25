from pydantic import BaseModel


class CarreraCreate(BaseModel):
    clave: int
    nombre: str


class CarreraUpdate(BaseModel):
    clave: int
    nombre: str


class CarreraOut(BaseModel):
    id: int
    clave: int
    nombre: str

    class Config:
        from_attributes = True
