from pydantic import BaseModel
from datetime import datetime

class EventoBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    fecha_evento: datetime
    fecha_venta_inicio: datetime
    fecha_venta_fin: datetime
    precio: float
    estado: str = "activo"
    sede_id: int

class EventoCreate(EventoBase):
    pass

class EventoUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    fecha_evento: datetime | None = None
    fecha_venta_inicio: datetime | None = None
    fecha_venta_fin: datetime | None = None
    precio: float | None = None
    estado: str | None = None

class EventoOut(EventoBase):
    evento_id: int

    class Config:
        from_attributes = True
