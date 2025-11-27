from pydantic import BaseModel
from datetime import datetime

class ReservaBase(BaseModel):
    usuario_id: int
    evento_id: int
    precio_total: float
    fecha_expiracion: datetime
    estado: str = "PENDIENTE"

class ReservaCreate(ReservaBase):
    asientos: list[int]

class ReservaUpdate(BaseModel):
    estado: str | None = None

class ReservaOut(ReservaBase):
    reserva_id: int

    class Config:
        from_attributes = True
