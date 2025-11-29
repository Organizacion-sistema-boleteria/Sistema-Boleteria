from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Boleto(Base):
    __tablename__ = "boletos"

    boleto_id = Column(Integer, primary_key=True, index=True)
    pago_id = Column(Integer, ForeignKey("pagos.pago_id"), nullable=False)
    asiento_id = Column(Integer, ForeignKey("asientos.asiento_id"), nullable=False)

    codigo_qr = Column(String, unique=True, nullable=False)
    
    # Estado: VALIDO, USADO, EXPIRADO
    estado = Column(String, default="VALIDO", nullable=False) 
    
    fecha_emision = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_uso = Column(DateTime, nullable=True) # Cuando el boleto es validado en el acceso

    # Relaciones
    pago = relationship("Pago", back_populates="boletos")
    asiento = relationship("Asiento")