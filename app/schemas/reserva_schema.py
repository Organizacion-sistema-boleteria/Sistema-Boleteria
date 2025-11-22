# app/schemas/reserva_schema.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ReservaBase(BaseModel):
    usuario_id: int
    evento_id: int
    fecha_expiracion: datetime
    estado: Optional[str] = "ACTIVA"
    precio_total: float


class ReservaCreate(ReservaBase):
    asientos_ids: List[int]


class ReservaUpdate(BaseModel):
    fecha_expiracion: Optional[datetime] = None
    estado: Optional[str] = None
    precio_total: Optional[float] = None
    asientos_ids: Optional[List[int]] = None


class ReservaResponse(ReservaBase):
    reserva_id: int
    fecha_reserva: datetime
    asientos: List[int]

    class Config:
        orm_mode = True
