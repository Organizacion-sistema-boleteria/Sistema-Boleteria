from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# --- Request: Crear Reserva (US-009) ---
class ReservaCreateRequest(BaseModel):
    evento_id: int
    asientos: List[int] # Lista de IDs de asientos a reservar
    
    # Ejemplo para Swagger
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "evento_id": 1,
                    "asientos": [15, 16, 17]
                }
            ]
        }
    }


# --- Response: Estructura interna de datos ---
class ReservaData(BaseModel):
    # Usamos Field(alias) para que la respuesta JSON use camelCase (reservaId, etc.)
    reserva_id: int = Field(..., alias="reservaId")
    usuario_id: int = Field(..., alias="usuarioId")
    evento_id: int = Field(..., alias="eventoId")
    
    asientosReservados: List[int] 
    precio_total: float = Field(..., alias="precioTotal")
    fecha_reserva: datetime = Field(..., alias="fechaReserva")
    fecha_expiracion: datetime = Field(..., alias="fechaExpiracion")
    estado: str

    class Config:
        from_attributes = True
        populate_by_name = True

# --- Response: Wrappers para endpoints ---
class ReservaResponse(BaseModel):
    success: bool
    message: str
    data: Optional[ReservaData] = None
    error_details: Optional[List[str]] = None 

class ReservaListResponse(BaseModel):
    success: bool
    message: str
    data: List[ReservaData]

# --- Response: Cancelación Automática (US-010) ---
class ExpiracionData(BaseModel):
    reservasCanceladas: int
    asientosLiberados: int
    fechaEjecucion: datetime

class ExpiracionResponse(BaseModel):
    success: bool
    message: str
    data: ExpiracionData