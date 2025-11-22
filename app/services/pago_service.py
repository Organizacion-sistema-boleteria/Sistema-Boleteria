# app/services/pago_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional

from app.repository.pago_repository import PagoRepository
from app.repository.reserva_repository import ReservaRepository
from app.repository.boleto_repository import BoletoRepository
from app.schemas.pago_schema import PagoCreate, PagoUpdate
from app.services.reserva_service import ReservaService
from app.services.asiento_service import AsientoService
from app.services.boleto_service import BoletoService


class PagoService:

    @staticmethod
    def create(db: Session, data: PagoCreate):
        # validar reserva
        reserva = ReservaRepository.get_by_id(db, data.reserva_id)
        if not reserva:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")

        # monto mínimo verificado con precio_total
        if float(data.monto) < float(reserva.precio_total):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="El monto es menor al precio total de la reserva")

        pago = PagoRepository.create(db, data)

        # Si el pago se crea en estado APROBADO => confirmar reserva y generar boletos
        if pago.estado == "APROBADO":
            # confirmar reserva
            reserva.estado = "CONFIRMADA"
            db.commit()
            db.refresh(reserva)

            # marcar asientos como vendidos
            for asiento in reserva.asientos:
                AsientoService.sell_seat(db, asiento.asiento_id)

            # generar boletos para cada asiento (automático)
            boletos_generados = []
            for asiento in reserva.asientos:
                boleto = BoletoService.create(db, {
                    "pago_id": pago.pago_id,
                    "asiento_id": asiento.asiento_id
                })
                boletos_generados.append(boleto)
            # retornar pago y boletos si deseas
            return {"pago": pago, "boletos": boletos_generados}

        return pago

    @staticmethod
    def get(db: Session, pago_id: int):
        pago = PagoRepository.get_by_id(db, pago_id)
        if not pago:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
        return pago

    @staticmethod
    def update(db: Session, pago_id: int, data: PagoUpdate):
        pago = PagoService.get(db, pago_id)
        previo_estado = pago.estado
        pago = PagoRepository.update(db, pago, data)

        # Si se cambia a APROBADO y anteriormente no lo estaba, ejecutar confirmaciones
        if previo_estado != "APROBADO" and pago.estado == "APROBADO":
            reserva = ReservaRepository.get_by_id(db, pago.reserva_id)
            if reserva:
                reserva.estado = "CONFIRMADA"
                db.commit()
                db.refresh(reserva)
                # marcar asientos vendidos
                for asiento in reserva.asientos:
                    AsientoService.sell_seat(db, asiento.asiento_id)
                # generar boletos
                boletos = []
                for asiento in reserva.asientos:
                    boleto = BoletoService.create(db, {
                        "pago_id": pago.pago_id,
                        "asiento_id": asiento.asiento_id
                    })
                    boletos.append(boleto)
                return {"pago": pago, "boletos": boletos}

        return pago

    @staticmethod
    def delete(db: Session, pago_id: int):
        pago = PagoService.get(db, pago_id)
        # Nota: si eliminas un pago aprobado debes definir políticas (aquí no revertimos ventas)
        PagoRepository.delete(db, pago)
        return {"message": "Pago eliminado correctamente"}
