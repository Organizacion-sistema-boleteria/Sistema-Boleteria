# app/services/reserva_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from datetime import datetime

from app.repository.reserva_repository import ReservaRepository
from app.repository.asiento_repository import AsientoRepository
from app.repository.usuario_repository import UsuarioRepository
from app.repository.evento_repository import EventoRepository
from app.domain.reserva_model import Reserva
from app.schemas.reserva_schema import ReservaCreate, ReservaUpdate
from app.services.asiento_service import AsientoService


class ReservaService:

    @staticmethod
    def create(db: Session, data: ReservaCreate) -> Reserva:
        # Validar usuario y evento
        usuario = UsuarioRepository.get_by_id(db, data.usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        evento = EventoRepository.get_by_id(db, data.evento_id)
        if not evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado"
            )

        # Validaciones sobre asientos: disponibilidad y existencia
        if not data.asientos_ids or len(data.asientos_ids) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La reserva debe incluir al menos un asiento"
            )

        # calcular precio_total sumando precios de asientos; validar disponibilidad
        total = 0.0
        for asiento_id in data.asientos_ids:
            asiento = AsientoRepository.get_by_id(db, asiento_id)
            if not asiento:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Asiento {asiento_id} no existe"
                )
            if asiento.evento_id != data.evento_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Asiento {asiento_id} no pertenece al evento {data.evento_id}"
                )
            if asiento.estado != "DISPONIBLE":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Asiento {asiento_id} no está disponible (estado={asiento.estado})"
                )
            total += float(asiento.precio)

        # crear reserva (precio_total calculado)
        reserva_payload = ReservaCreate(
            usuario_id=data.usuario_id,
            evento_id=data.evento_id,
            fecha_expiracion=data.fecha_expiracion,
            estado=data.estado,
            precio_total=total,
            asientos_ids=data.asientos_ids
        )

        reserva = ReservaRepository.create(db, reserva_payload)

        # marcar asientos como RESERVADO
        for asiento_id in data.asientos_ids:
            AsientoService.reserve_seat(db, asiento_id)

        return reserva

    @staticmethod
    def get(db: Session, reserva_id: int) -> Reserva:
        reserva = ReservaRepository.get_by_id(db, reserva_id)
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        return reserva

    @staticmethod
    def list(db: Session):
        return ReservaRepository.list(db)

    @staticmethod
    def update(db: Session, reserva_id: int, data: ReservaUpdate):
        reserva = ReservaService.get(db, reserva_id)

        # Si se modifican asientos, validarlos y reservar/actualizar estados
        if data.asientos_ids is not None:
            # liberar asientos actuales
            # busco asientos ligados a la reserva
            current_asientos = [a.asiento_id for a in reserva.asientos]
            for asiento_id in current_asientos:
                # solo liberar si estaban en estado RESERVADO
                try:
                    AsientoService.release_seat(db, asiento_id)
                except HTTPException:
                    pass

            # validar y reservar nuevos asientos
            total = 0.0
            for asiento_id in data.asientos_ids:
                asiento = AsientoRepository.get_by_id(db, asiento_id)
                if not asiento:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"Asiento {asiento_id} no existe")
                if asiento.estado != "DISPONIBLE":
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail=f"Asiento {asiento_id} no está disponible")
                total += float(asiento.precio)
                AsientoService.reserve_seat(db, asiento_id)

            data_dict = data.model_dump(exclude_unset=True)
            data_dict["precio_total"] = total
            updated = ReservaRepository.update(db, reserva, ReservaUpdate(**data_dict))
            return updated

        # actualizaciones simples
        return ReservaRepository.update(db, reserva, data)

    @staticmethod
    def delete(db: Session, reserva_id: int):
        reserva = ReservaService.get(db, reserva_id)
        # liberar asientos asociados si estaban reservados
        for asiento in reserva.asientos:
            try:
                AsientoService.release_seat(db, asiento.asiento_id)
            except HTTPException:
                pass
        ReservaRepository.delete(db, reserva)
        return {"message": "Reserva eliminada correctamente"}

    @staticmethod
    def expire_reservations(db: Session):
        """
        Método utilitario: buscar reservas expiradas y liberarlas.
        No está programado para correr automáticamente aquí (no background),
        pero puedes llamarlo desde un endpoint administrativo o desde un job externo.
        """
        now = datetime.utcnow()
        expiradas = db.query(Reserva).filter(Reserva.fecha_expiracion < now, Reserva.estado == "ACTIVA").all()
        for r in expiradas:
            # liberar asientos
            for asiento in r.asientos:
                try:
                    AsientoService.release_seat(db, asiento.asiento_id)
                except Exception:
                    pass
            r.estado = "EXPIRADA"
        db.commit()
        return len(expiradas)
