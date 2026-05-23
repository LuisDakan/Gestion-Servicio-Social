from pydantic import BaseModel


class CarreraCreate(BaseModel):
    nombre: str


class CarreraUpdate(BaseModel):
    nombre: str


class CarreraOut(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True
