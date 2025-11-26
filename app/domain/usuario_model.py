from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telefono = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    rol = Column(String, nullable=False, default="CLIENTE")
    estado = Column(String, nullable=False, default="ACTIVO")
    fecha_registro = Column(DateTime, default=datetime.utcnow)
