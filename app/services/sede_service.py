# app/services/sede_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repository.sede_repository import SedeRepository
from app.schemas.sede_schema import SedeCreate, SedeUpdate


class SedeService:

    @staticmethod
    def create(db: Session, data: SedeCreate):
        return SedeRepository.create(db, data)

    @staticmethod
    def get(db: Session, sede_id: int):
        sede = SedeRepository.get_by_id(db, sede_id)
        if not sede:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sede no encontrada"
            )
        return sede

    @staticmethod
    def list(db: Session):
        return SedeRepository.list(db)

    @staticmethod
    def update(db: Session, sede_id: int, data: SedeUpdate):
        sede = SedeService.get(db, sede_id)
        return SedeRepository.update(db, sede, data)

    @staticmethod
    def delete(db: Session, sede_id: int):
        sede = SedeService.get(db, sede_id)
        SedeRepository.delete(db, sede)
        return {"message": "Sede eliminada correctamente"}
