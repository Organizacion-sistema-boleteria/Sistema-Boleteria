from pydantic import BaseModel

class BoletoBase(BaseModel):
    qr: str
    estado: str = "VALIDO"
    asiento_id: int
    usuario_id: int

class BoletoCreate(BoletoBase):
    pass

class BoletoOut(BoletoBase):
    boleto_id: int

    class Config:
        from_attributes = True
