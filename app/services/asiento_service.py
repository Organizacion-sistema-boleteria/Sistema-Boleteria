# app/services/asiento_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.repository.asiento_repository import AsientoRepository
from app.repository.evento_repository import EventoRepository
from app.schemas.asiento_schema import AsientoCreate, AsientoUpdate
from app.domain.asiento_model import Asiento


class AsientoService:

    @staticmethod
    def create(db: Session, data: AsientoCreate) -> Asiento:
        # validar evento existe
        evento = EventoRepository.get_by_id(db, data.evento_id)
        if not evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado para asignar el asiento"
            )
        return AsientoRepository.create(db, data)

    @staticmethod
    def get(db: Session, asiento_id: int) -> Asiento:
        asiento = AsientoRepository.get_by_id(db, asiento_id)
        if not asiento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asiento no encontrado"
            )
        return asiento

    @staticmethod
    def list_by_evento(db: Session, evento_id: int) -> List[Asiento]:
        return AsientoRepository.list_by_evento(db, evento_id)

    @staticmethod
    def update(db: Session, asiento_id: int, data: AsientoUpdate) -> Asiento:
        asiento = AsientoService.get(db, asiento_id)
        # no permitir cambiar a DISPONIBLE si está VENDIDO (regla de negocio)
        if "estado" in data.model_dump(exclude_unset=True):
            nuevo_estado = data.model_dump(exclude_unset=True)["estado"]
            if asiento.estado == "VENDIDO" and nuevo_estado != "VENDIDO":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se puede cambiar el estado de un asiento vendido"
                )
        return AsientoRepository.update(db, asiento, data)

    @staticmethod
    def delete(db: Session, asiento_id: int):
        asiento = AsientoService.get(db, asiento_id)
        if asiento.estado == "VENDIDO":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar un asiento vendido"
            )
        AsientoRepository.delete(db, asiento)
        return {"message": "Asiento eliminado correctamente"}

    # utilidades usadas por otros services
    @staticmethod
    def reserve_seat(db: Session, asiento_id: int):
        asiento = AsientoService.get(db, asiento_id)
        if asiento.estado != "DISPONIBLE":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Asiento {asiento_id} no está disponible (estado={asiento.estado})"
            )
        asiento.estado = "RESERVADO"
        db.commit()
        db.refresh(asiento)
        return asiento

    @staticmethod
    def release_seat(db: Session, asiento_id: int):
        asiento = AsientoService.get(db, asiento_id)
        # Sólo liberamos si está RESERVADO (no revertir boletos vendidos)
        if asiento.estado == "RESERVADO":
            asiento.estado = "DISPONIBLE"
            db.commit()
            db.refresh(asiento)
        return asiento

    @staticmethod
    def sell_seat(db: Session, asiento_id: int):
        asiento = AsientoService.get(db, asiento_id)
        if asiento.estado == "VENDIDO":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Asiento {asiento_id} ya está vendido"
            )
        # sólo vender si está reservado o disponible (venta directa posible)
        asiento.estado = "VENDIDO"
        db.commit()
        db.refresh(asiento)
        return asiento
