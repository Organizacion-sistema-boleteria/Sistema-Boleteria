from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repository.sede_repository import SedeRepository
from app.schemas.sede_schema import SedeCreate, SedeUpdate, SedeOut

class SedeService:

    @staticmethod
    def get_all(db: Session):
        return SedeRepository.list(db)

    @staticmethod
    def get_by_id(db: Session, sede_id: int):
        sede = SedeRepository.get_by_id(db, sede_id)
        if not sede:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "message": "Sede no encontrada",
                    "error": {"code": 404, "details": f"No se encontró una sede con ID {sede_id}"}
                }
            )
        return sede

    @staticmethod
    def create(db: Session, data: SedeCreate) -> SedeOut:
        try:
            return SedeRepository.create(db, data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "success": False, 
                    "message": "Error interno", 
                    "error": {"code": 500, "details": str(e)}
                }
            )

    @staticmethod
    def update(db: Session, sede_id: int, data: SedeUpdate):
        # Primero verificamos que exista
        sede = SedeService.get_by_id(db, sede_id)
        return SedeRepository.update(db, sede, data)

    @staticmethod
    def delete(db: Session, sede_id: int):
        # Primero verificamos que exista
        sede = SedeService.get_by_id(db, sede_id)
        # Aquí podrías validar si la sede tiene eventos futuros antes de borrarla
        SedeRepository.delete(db, sede)