from pydantic import BaseModel

class ReporteOut(BaseModel):
    titulo: str
    total_ventas: float | None = None
    total_eventos: int | None = None
    total_boletos: int | None = None
    detalles: dict | None = None
