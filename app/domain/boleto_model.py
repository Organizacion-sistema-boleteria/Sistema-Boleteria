# app/domain/boleto_model.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Boleto(Base):
    __tablename__ = "boletos"

    boleto_id = Column(Integer, primary_key=True, index=True)
    pago_id = Column(Integer, ForeignKey("pagos.pago_id"), nullable=False)
    asiento_id = Column(Integer, ForeignKey("asientos.asiento_id"), nullable=False)

    codigo_qr = Column(String, unique=True, nullable=False)
    fecha_emision = Column(DateTime, server_default=func.now())
    estado = Column(String, default="VALIDO")  # VALIDO, USADO, EXPIRADO
    fecha_uso = Column(DateTime, nullable=True)

    pago = relationship("Pago")
    asiento = relationship("Asiento")
