# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator
import os

# Ruta por defecto para la DB sqlite (archivo en el root del proyecto)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLITE_FILE = os.getenv("SQLITE_FILE", os.path.join(BASE_DIR, "app.db"))

DATABASE_URL = f"sqlite:///{SQLITE_FILE}"

# Nota: echo=True durante desarrollo puede ayudar para ver SQL generada
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # requerido por SQLite + threads
    echo=False,
)

# SessionLocal: factories de sesión (scope por request)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

# Base para los modelos declarativos
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency de FastAPI para obtener una sesión de DB por request.
    Uso en endpoints:
        from fastapi import Depends
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Inicializa la base de datos creando las tablas definidas en los modelos.
    Importante: antes de llamar a init_db() debes importar los módulos donde están
    definidos los modelos (para que Base.metadata los conozca).
    Ejemplo de uso:
        from app import models  # importa tus modelos para registrarlos
        init_db()
    """
    Base.metadata.create_all(bind=engine)
