# app/domain/usuario_model.py
from sqlalchemy import Column, Integer, String
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telefono = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)  # <── ESTA ES LA COLUMNA REAL
    rol = Column(String, nullable=False)
    estado = Column(String, nullable=False)
