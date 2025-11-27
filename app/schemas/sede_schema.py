from pydantic import BaseModel, field_validator
from typing import Optional

# Base Schema: Campos comunes
class SedeBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    ciudad: str
    capacidad_total: int
    descripcion: Optional[str] = None
    estado: str = "ACTIVA"

    @field_validator("capacidad_total")
    def validar_capacidad_total(cls, v: int):
        if v <= 0:
            raise ValueError("La capacidad total debe ser un número positivo mayor a 0.")
        return v

# Schema para CREAR (POST)
class SedeCreate(SedeBase):
    pass

# Schema para ACTUALIZAR (PUT) - Todos opcionales
class SedeUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    capacidad_total: Optional[int] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None

# Schema para RESPUESTA (GET)
class SedeOut(BaseModel):
    sede_id: int
    nombre: str
    direccion: Optional[str]
    ciudad: str
    capacidad_total: int
    descripcion: Optional[str]
    estado: str

    class Config:
        from_attributes = True