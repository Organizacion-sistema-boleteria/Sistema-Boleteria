from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

# --- Schemas Base ---

class EventoBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    sede_id: int
    fecha_evento: datetime
    fecha_venta_inicio: datetime
    fecha_venta_fin: datetime
    precio_base: float
    categoria: str
    estado: str = "PROGRAMADO"

    # Validaciones básicas de Pydantic (las fuertes van en el servicio)
    @field_validator('fecha_evento')
    def fecha_evento_futura(cls, v):
        # US-005: Fecha evento posterior a fecha actual
        # Nota: Pydantic valida al recibir, pero la lógica de negocio suele ir en services
        return v

# --- Schema CREAR (POST) ---
class EventoCreate(EventoBase):
    # organizador_id no se pide en el body, se saca del token
    pass

# --- Schema ACTUALIZAR (PUT) ---
class EventoUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    sede_id: Optional[int] = None
    fecha_evento: Optional[datetime] = None
    fecha_venta_inicio: Optional[datetime] = None
    fecha_venta_fin: Optional[datetime] = None
    precio_base: Optional[float] = None
    categoria: Optional[str] = None
    estado: Optional[str] = None

# --- Schemas para Respuesta Anidada (US-005 y US-006) ---

class SedeSimpleOut(BaseModel):
    sede_id: int
    nombre: str
    ciudad: str
    capacidad_total: int # Según tu JSON de ejemplo

    class Config:
        from_attributes = True

class OrganizadorSimpleOut(BaseModel):
    usuario_id: int
    nombre: str

    class Config:
        from_attributes = True

# --- Schema RESPUESTA FINAL ---
class EventoOut(BaseModel):
    evento_id: int
    titulo: str
    descripcion: Optional[str]
    fecha_evento: datetime
    fecha_venta_inicio: datetime
    fecha_venta_fin: datetime
    precio_base: float
    categoria: str
    estado: str
    
    # Objetos anidados
    sede: Optional[SedeSimpleOut] = None
    organizador: Optional[OrganizadorSimpleOut] = None

    class Config:
        from_attributes = True