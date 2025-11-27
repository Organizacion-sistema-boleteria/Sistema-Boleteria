# app/domain/pago_model.py
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Pago(Base):
    __tablename__ = "pagos"

    pago_id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(Integer, ForeignKey("reservas.reserva_id"), unique=True)

    monto = Column(Float, nullable=False)
    metodo_pago = Column(String, nullable=False)
    estado = Column(String, default="PENDIENTE")  # PENDIENTE, APROBADO, RECHAZADO
    fecha_pago = Column(DateTime, server_default=func.now())
    referencia_externa = Column(String, nullable=True)

    reserva = relationship("Reserva")
