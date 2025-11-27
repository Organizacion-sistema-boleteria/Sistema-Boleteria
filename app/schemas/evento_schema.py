from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

# --- Schemas Base ---

class EventoBase(BaseModel):
    # Campos obligatorios
    sede_id: int
    # organizador_id NO va aquí para creación, se maneja internamente
    titulo: str
    fecha_evento: datetime
    fecha_venta_inicio: datetime
    fecha_venta_fin: datetime
    precio_base: float
    categoria: str
    
    # Campos opcionales con default
    descripcion: Optional[str] = None
    estado: str = "PROGRAMADO"

    @field_validator('fecha_venta_inicio', 'fecha_venta_fin', 'fecha_evento')
    def validar_cronologia_fechas(cls, v, info):
        # La validación fuerte se hace en el servicio
        return v

# --- Schema CREAR (POST) ---
class EventoCreate(EventoBase):
    # organizador_id se obtiene del token, no del body
    
    # ESTA ES LA MAGIA: Configuración para el ejemplo en Swagger
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "titulo": "Festival de Verano 2026",
                    "descripcion": "El evento musical más grande del año con artistas internacionales.",
                    "sede_id": 1,
                    "fecha_evento": "2026-06-20T20:00:00",
                    "fecha_venta_inicio": "2026-01-15T08:00:00",
                    "fecha_venta_fin": "2026-06-20T15:00:00",
                    "precio_base": 250000.00,
                    "categoria": "CONCIERTO",
                    "estado": "PROGRAMADO"
                }
            ]
        }
    }

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
    capacidad_total: int

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