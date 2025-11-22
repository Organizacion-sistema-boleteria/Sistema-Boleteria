# app/schemas/pago_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PagoBase(BaseModel):
    reserva_id: int
    monto: float
    metodo_pago: str
    estado: Optional[str] = "PENDIENTE"
    referencia_externa: Optional[str] = None


class PagoCreate(PagoBase):
    pass


class PagoUpdate(BaseModel):
    monto: Optional[float] = None
    metodo_pago: Optional[str] = None
    estado: Optional[str] = None
    referencia_externa: Optional[str] = None


class PagoResponse(PagoBase):
    pago_id: int
    fecha_pago: datetime

    class Config:
        orm_mode = True
