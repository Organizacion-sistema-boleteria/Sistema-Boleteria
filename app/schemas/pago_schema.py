from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# --- Schemas de Boleto (Respuesta Anidada) ---
class BoletoSimpleOut(BaseModel):
    boleto_id: int = Field(alias="boletoId")
    codigo_qr: str = Field(alias="codigoQR")
    estado: str

    class Config:
        from_attributes = True
        populate_by_name = True

# --- Schemas de PAGO ---
class PagoRequest(BaseModel):
    reserva_id: int = Field(alias="reservaId")
    metodo_pago: str = Field(alias="metodoPago")
    monto_solicitado: float = Field(alias="monto") # Se usa para verificación

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "reservaId": 101,
                    "metodoPago": "TARJETA_CREDITO",
                    "monto": 150000.00
                }
            ]
        }
    }

class PagoOut(BaseModel):
    pago_id: int = Field(alias="pagoId")
    reserva_id: int = Field(alias="reservaId")
    monto: float
    metodo_pago: str = Field(alias="metodoPago")
    estado: str
    fecha_pago: datetime = Field(alias="fechaPago")
    referencia_externa: Optional[str] = Field(None, alias="referenciaExterna")
    
    # Nuevo para US-012
    intentos: int
    
    # Anidado: Lista de boletos generados (solo en respuesta APROBADA)
    boletos_generados: Optional[List[BoletoSimpleOut]] = Field(None, alias="boletosGenerados")

    class Config:
        from_attributes = True
        populate_by_name = True