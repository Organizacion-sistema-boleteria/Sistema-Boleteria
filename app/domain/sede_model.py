from sqlalchemy import Column, Integer, String
from app.database import Base

class Sede(Base):
    __tablename__ = "sede"

    sede_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=True)
    ciudad = Column(String, nullable=False)
    capacidad_total = Column(Integer, nullable=False)
    descripcion = Column(String, nullable=True)
    estado = Column(String, nullable=False, default="ACTIVA")
