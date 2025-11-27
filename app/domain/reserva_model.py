# app/domain/reserva_model.py
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base, engine

# TABLA INTERMEDIA N:M
Reserva_Asiento = Table(
    "reserva_asiento",
    Base.metadata,
    Column("reserva_id", Integer, ForeignKey("reservas.reserva_id"), primary_key=True),
    Column("asiento_id", Integer, ForeignKey("asientos.asiento_id"), primary_key=True),
)

class Reserva(Base):
    __tablename__ = "reservas"

    reserva_id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    evento_id = Column(Integer, ForeignKey("eventos.evento_id"), nullable=False)

    fecha_reserva = Column(DateTime, server_default=func.now())
    fecha_expiracion = Column(DateTime, nullable=False)

    estado = Column(String, default="ACTIVA")  # ACTIVA, CONFIRMADA, EXPIRADA, CANCELADA
    precio_total = Column(Float, nullable=False)

    usuario = relationship("Usuario")
    evento = relationship("Evento")
    asientos = relationship("Asiento", secondary=Reserva_Asiento)
