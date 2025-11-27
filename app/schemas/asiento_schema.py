from pydantic import BaseModel

class AsientoBase(BaseModel):
    fila: str
    numero: int
    estado: str = "DISPONIBLE"
    evento_id: int

class AsientoCreate(AsientoBase):
    pass

class AsientoUpdate(BaseModel):
    fila: str | None = None
    numero: int | None = None
    estado: str | None = None

class AsientoOut(AsientoBase):
    asiento_id: int

    class Config:
        from_attributes = True
