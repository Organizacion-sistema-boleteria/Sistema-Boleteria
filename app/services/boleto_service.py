# app/services/boleto_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
import uuid

from app.repository.boleto_repository import BoletoRepository
from app.repository.pago_repository import PagoRepository
from app.repository.asiento_repository import AsientoRepository
from app.schemas.boleto_schema import BoletoCreate, BoletoUpdate
from app.domain.boleto_model import Boleto


class BoletoService:

    @staticmethod
    def create(db: Session, data) -> Boleto:
        """
        data puede ser un dict con keys: pago_id, asiento_id
        o un objeto Pydantic BoletoCreate.
        Se genera codigo_qr automáticamente si no se pasa.
        """
        payload = {}
        if isinstance(data, dict):
            payload["pago_id"] = data.get("pago_id")
            payload["asiento_id"] = data.get("asiento_id")
            payload["codigo_qr"] = data.get("codigo_qr") or str(uuid.uuid4())
            payload["estado"] = data.get("estado", "VALIDO")
            payload["fecha_uso"] = data.get("fecha_uso", None)
        else:
            # esperar que sea un Pydantic
            payload = data.model_dump()

        # validar pago y asiento
        pago = PagoRepository.get_by_id(db, payload["pago_id"])
        if not pago:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")

        asiento = AsientoRepository.get_by_id(db, payload["asiento_id"])
        if not asiento:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asiento no encontrado")

        # crear boleto
        boleto_data = BoletoCreate(
            pago_id=payload["pago_id"],
            asiento_id=payload["asiento_id"],
            codigo_qr=payload["codigo_qr"],
            estado=payload.get("estado", "VALIDO"),
            fecha_uso=payload.get("fecha_uso", None)
        )
        boleto = BoletoRepository.create(db, boleto_data)
        return boleto

    @staticmethod
    def get(db: Session, boleto_id: int):
        boleto = BoletoRepository.get_by_id(db, boleto_id)
        if not boleto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Boleto no encontrado")
        return boleto

    @staticmethod
    def list(db: Session):
        return BoletoRepository.list(db)

    @staticmethod
    def validate_by_qr(db: Session, codigo_qr: str):
        boleto = db.query(Boleto).filter(Boleto.codigo_qr == codigo_qr).first()
        if not boleto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Boleto no encontrado")

        if boleto.estado != "VALIDO":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Boleto no válido (estado={boleto.estado})")

        boleto.estado = "USADO"
        boleto.fecha_uso = datetime.utcnow()
        db.commit()
        db.refresh(boleto)
        return boleto

    @staticmethod
    def update(db: Session, boleto_id: int, data: BoletoUpdate):
        boleto = BoletoService.get(db, boleto_id)
        return BoletoRepository.update(db, boleto, data)

    @staticmethod
    def delete(db: Session, boleto_id: int):
        boleto = BoletoService.get(db, boleto_id)
        BoletoRepository.delete(db, boleto)
        return {"message": "Boleto eliminado correctamente"}
