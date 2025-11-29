from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Asiento(Base):
    __tablename__ = "asientos"

    asiento_id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, ForeignKey("eventos.evento_id"), nullable=False)
    
    # NUEVO: Llave foránea a la reserva
    reserva_id = Column(Integer, ForeignKey("reservas.reserva_id"), nullable=True) 

    seccion = Column(String, nullable=False)
    fila = Column(String, nullable=False)
    numero = Column(String, nullable=False)

    precio = Column(Float, nullable=False)
    tipo = Column(String, nullable=False)
    estado = Column(String, default="DISPONIBLE") 

    evento = relationship("Evento", back_populates="asientos")
    # NUEVO: Relación inversa para vincular a la reserva
    reserva = relationship("Reserva", back_populates="asientos")