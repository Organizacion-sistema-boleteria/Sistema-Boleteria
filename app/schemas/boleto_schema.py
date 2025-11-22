# app/schemas/boleto_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BoletoBase(BaseModel):
    pago_id: int
    asiento_id: int
    codigo_qr: str
    estado: Optional[str] = "VALIDO"
    fecha_uso: Optional[datetime] = None


class BoletoCreate(BoletoBase):
    pass


class BoletoUpdate(BaseModel):
    estado: Optional[str] = None
    fecha_uso: Optional[datetime] = None


class BoletoResponse(BoletoBase):
    boleto_id: int
    fecha_emision: datetime

    class Config:
        orm_mode = True
