from pydantic import BaseModel
from datetime import datetime

class PagoBase(BaseModel):
    reserva_id: int
    monto: float
    metodo_pago: str
    fecha_pago: datetime | None = None
    estado: str = "COMPLETADO"

class PagoCreate(PagoBase):
    pass

class PagoOut(PagoBase):
    pago_id: int

    class Config:
        from_attributes = True
