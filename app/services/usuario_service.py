# app/services/usuario_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repository.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate


class UsuarioService:

    @staticmethod
    def create(db: Session, data: UsuarioCreate):
        # Validar email duplicado
        exist = UsuarioRepository.get_by_email(db, data.email)
        if exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado."
            )

        return UsuarioRepository.create(db, data)

    @staticmethod
    def get(db: Session, user_id: int):
        user = UsuarioRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return user

    @staticmethod
    def list(db: Session):
        return UsuarioRepository.list(db)

    @staticmethod
    def update(db: Session, user_id: int, data: UsuarioUpdate):
        user = UsuarioService.get(db, user_id)
        return UsuarioRepository.update(db, user, data)

    @staticmethod
    def delete(db: Session, user_id: int):
        user = UsuarioService.get(db, user_id)
        UsuarioRepository.delete(db, user)
        return {"message": "Usuario eliminado correctamente"}
