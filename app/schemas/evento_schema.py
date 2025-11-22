# app/schemas/evento_schema.py
from pydantic import BaseModel
from datetime import datetime

class EventoBase(BaseModel):
    sede_id: int
    organizador_id: int
    titulo: str
    descripcion: str | None = None
    fecha_evento: datetime
    fecha_venta_inicio: datetime
    fecha_venta_fin: datetime
    precio_base: float
    categoria: str

class EventoCreate(EventoBase):
    pass

class EventoUpdate(BaseModel):
    titulo: str | None = None
    descripcion: str | None = None
    fecha_evento: datetime | None = None
    fecha_venta_inicio: datetime | None = None
    fecha_venta_fin: datetime | None = None
    precio_base: float | None = None
    categoria: str | None = None
    estado: str | None = None

class EventoResponse(EventoBase):
    evento_id: int
    estado: str

    class Config:
        from_attributes = True
