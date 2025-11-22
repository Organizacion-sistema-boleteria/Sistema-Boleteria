# app/schemas/sede_schema.py
from pydantic import BaseModel

class SedeBase(BaseModel):
    nombre: str
    direccion: str
    ciudad: str
    capacidad_total: int
    descripcion: str | None = None

class SedeCreate(SedeBase):
    pass

class SedeUpdate(BaseModel):
    nombre: str | None = None
    direccion: str | None = None
    ciudad: str | None = None
    capacidad_total: int | None = None
    descripcion: str | None = None
    estado: str | None = None

class SedeResponse(SedeBase):
    sede_id: int
    estado: str

    class Config:
        from_attributes = True
