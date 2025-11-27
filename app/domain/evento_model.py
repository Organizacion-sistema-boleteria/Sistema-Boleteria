# app/domain/evento_model.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Evento(Base):
    __tablename__ = "eventos"

    evento_id = Column(Integer, primary_key=True, index=True)
    # CORRECCIÓN y relación bidireccional
    sede_id = Column(Integer, ForeignKey("sede.sede_id"), nullable=False)
    organizador_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)

    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)

    fecha_evento = Column(DateTime, nullable=False)
    fecha_venta_inicio = Column(DateTime, nullable=False)
    fecha_venta_fin = Column(DateTime, nullable=False)

    precio_base = Column(Float, nullable=False)
    categoria = Column(String, nullable=False)
    estado = Column(String, default="PROGRAMADO")

    # Usar back_populates para la relación bidireccional
    sede = relationship("Sede", back_populates="eventos")
    organizador = relationship("Usuario")