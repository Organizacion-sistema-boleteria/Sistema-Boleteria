from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Reserva(Base):
    __tablename__ = "reservas"

    reserva_id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    evento_id = Column(Integer, ForeignKey("eventos.evento_id"), nullable=False)

    precio_total = Column(Float, nullable=False)
    fecha_reserva = Column(DateTime, default=datetime.utcnow) 
    fecha_expiracion = Column(DateTime, nullable=False)
    
    estado = Column(String, default="PENDIENTE")

    usuario = relationship("Usuario")
    evento = relationship("Evento")
    asientos = relationship("Asiento", back_populates="reserva")