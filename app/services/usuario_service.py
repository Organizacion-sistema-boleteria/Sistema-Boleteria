from sqlalchemy.orm import Session
from fastapi import HTTPException
import re

from app.repository.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate
from app.core.security import hash_password


class UsuarioService:

    @staticmethod
    def validar_password(password: str):
        if len(password) < 8 or \
           not re.search(r"[A-Z]", password) or \
           not re.search(r"[a-z]", password) or \
           not re.search(r"[0-9]", password):

            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": "Contraseña inválida",
                    "error": {
                        "code": 400,
                        "details": "La contraseña debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas y números"
                    }
                }
            )

    @staticmethod
    def create(db: Session, data: UsuarioCreate):

        # Email duplicado
        if UsuarioRepository.get_by_email(db, data.email):
            raise HTTPException(
                status_code=409,
                detail={
                    "success": False,
                    "message": "El email ya está registrado",
                    "error": {
                        "code": 409,
                        "details": f"El email {data.email} ya existe en el sistema"
                    }
                }
            )

        # Validar contraseña fuerte
        UsuarioService.validar_password(data.password)

        password_hash = hash_password(data.password)

        return UsuarioRepository.create(db, data, password_hash)

    @staticmethod
    def get_all(db: Session):
        return UsuarioRepository.list(db)

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return UsuarioRepository.get_by_id(db, user_id)

    @staticmethod
    def update(db: Session, user_id: int, data: UsuarioUpdate):
        usuario = UsuarioRepository.get_by_id(db, user_id)
        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return UsuarioRepository.update(db, usuario, data)

    @staticmethod
    def delete(db: Session, user_id: int):
        usuario = UsuarioRepository.get_by_id(db, user_id)
        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        UsuarioRepository.delete(db, usuario)
