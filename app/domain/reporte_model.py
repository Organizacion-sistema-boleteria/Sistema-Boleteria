# app/domain/reporte_model.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Reporte(Base):
    __tablename__ = "reportes"

    reporte_id = Column(Integer, primary_key=True, index=True)
    tipo_reporte = Column(String, nullable=False)
    evento_id = Column(Integer, ForeignKey("eventos.evento_id"), nullable=True)
    generado_por = Column(Integer, ForeignKey("usuarios.usuario_id"))

    fecha_generacion = Column(DateTime, server_default=func.now())
    parametros = Column(Text, nullable=True)
    datos = Column(Text, nullable=True)

    evento = relationship("Evento")
    usuario = relationship("Usuario")
