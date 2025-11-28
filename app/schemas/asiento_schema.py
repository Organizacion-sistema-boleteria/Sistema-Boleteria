from pydantic import BaseModel, field_validator
from typing import List, Optional

class FilaInput(BaseModel):
    fila: str
    asientos: int
    @field_validator('asientos')
    def v_cant(cls, v): return v if v > 0 else ValueError("Debe ser > 0")

class SeccionInput(BaseModel):
    nombre: str
    tipo: str
    precio: float
    filas: List[FilaInput]
    @field_validator('precio')
    def v_precio(cls, v): return v if v >= 0 else ValueError("Precio >= 0")

class AsientosCreateRequest(BaseModel):
    secciones: List[SeccionInput]

class AsientoUpdate(BaseModel):
    precio: Optional[float] = None
    tipo: Optional[str] = None
    estado: Optional[str] = None

class AsientoOut(BaseModel):
    asiento_id: int
    evento_id: int
    seccion: str
    fila: str
    numero: str
    precio: float
    tipo: str
    estado: str
    class Config: from_attributes = True

class DistribucionItem(BaseModel):
    seccion: str
    cantidad: int
    precio: float

class ResumenCreacionData(BaseModel):
    eventoId: int
    titulo: str
    totalAsientosCreados: int
    capacidadSede: int
    disponible: bool = True
    distribucion: List[DistribucionItem]

class DisponibilidadData(BaseModel):
    eventoId: int
    titulo: str
    fechaEvento: str 
    totalAsientos: int
    disponibles: int
    reservados: int
    vendidos: int
    asientos: List[AsientoOut]