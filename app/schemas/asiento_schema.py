# app/schemas/asiento_schema.py
from pydantic import BaseModel
from typing import Optional


class AsientoBase(BaseModel):
    evento_id: int
    seccion: str
    fila: str
    numero: str
    precio: float
    tipo: str
    estado: Optional[str] = "DISPONIBLE"


class AsientoCreate(AsientoBase):
    pass


class AsientoUpdate(BaseModel):
    seccion: Optional[str] = None
    fila: Optional[str] = None
    numero: Optional[str] = None
    precio: Optional[float] = None
    tipo: Optional[str] = None
    estado: Optional[str] = None


class AsientoResponse(AsientoBase):
    asiento_id: int

    class Config:
        orm_mode = True
