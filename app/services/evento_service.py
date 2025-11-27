# app/services/evento_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repository.evento_repository import EventoRepository
from app.repository.sede_repository import SedeRepository
from app.repository.usuario_repository import UsuarioRepository
from app.schemas.evento_schema import EventoCreate, EventoUpdate


class EventoService:

    @staticmethod
    def create(db: Session, data: EventoCreate):

        # Validar sede existente
        sede = SedeRepository.get_by_id(db, data.sede_id)
        if not sede:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La sede no existe"
            )

        # Validar organizador
        org = UsuarioRepository.get_by_id(db, data.organizador_id)
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El organizador no existe"
            )

        # Validar fechas
        if data.fecha_venta_inicio >= data.fecha_venta_fin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de inicio de venta debe ser anterior a fin de venta"
            )

        if data.fecha_venta_fin >= data.fecha_evento:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La venta no puede terminar después del evento"
            )

        return EventoRepository.create(db, data)

    @staticmethod
    def get(db: Session, evento_id: int):
        evento = EventoRepository.get_by_id(db, evento_id)
        if not evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado"
            )
        return evento

    @staticmethod
    def list(db: Session):
        return EventoRepository.list(db)

    @staticmethod
    def update(db: Session, evento_id: int, data: EventoUpdate):
        evento = EventoService.get(db, evento_id)
        return EventoRepository.update(db, evento, data)

    @staticmethod
    def delete(db: Session, evento_id: int):
        evento = EventoService.get(db, evento_id)
        EventoRepository.delete(db, evento)
        return {"message": "Evento eliminado correctamente"}
