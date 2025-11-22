# app/schemas/reporte_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReporteBase(BaseModel):
    tipo_reporte: str
    evento_id: Optional[int] = None
    generado_por: int
    parametros: Optional[str] = None
    datos: Optional[str] = None


class ReporteCreate(ReporteBase):
    pass


class ReporteUpdate(BaseModel):
    tipo_reporte: Optional[str] = None
    evento_id: Optional[int] = None
    parametros: Optional[str] = None
    datos: Optional[str] = None


class ReporteResponse(ReporteBase):
    reporte_id: int
    fecha_generacion: datetime

    class Config:
        orm_mode = True
