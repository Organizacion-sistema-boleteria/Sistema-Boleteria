from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Pago(Base):
    __tablename__ = "pagos"

    pago_id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(Integer, ForeignKey("reservas.reserva_id"), nullable=False)

    monto = Column(Float, nullable=False)
    metodo_pago = Column(String, nullable=False) # TARJETA_CREDITO, PSE, NEQUI, EFECTIVO, MOCK
    
    # NUEVO CAMPO para US-012
    intentos = Column(Integer, default=1, nullable=False) 
    
    # Estado: APROBADO, RECHAZADO, PENDIENTE, REEMBOLSADO
    estado = Column(String, default="PENDIENTE", nullable=False) 
    
    fecha_pago = Column(DateTime, default=datetime.utcnow, nullable=False)
    referencia_externa = Column(String, nullable=True) # Referencia de la pasarela

    # Relaciones
    reserva = relationship("Reserva")
    boletos = relationship("Boleto", back_populates="pago", cascade="all, delete-orphan")