from sqlalchemy.orm import Session
from app.domain.pago_model import Pago
from app.schemas.pago_schema import PagoRequest
from datetime import datetime

class PagoRepository:
    
    @staticmethod
    def get_by_id(db: Session, pago_id: int):
        return db.query(Pago).filter(Pago.pago_id == pago_id).first()

    @staticmethod
    def create(db: Session, reserva_id: int, monto: float, metodo: str, estado: str, ref_externa: str, intentos: int = 1):
        pago = Pago(
            reserva_id=reserva_id,
            monto=monto,
            metodo_pago=metodo,
            estado=estado,
            fecha_pago=datetime.utcnow(),
            referencia_externa=ref_externa,
            intentos=intentos
        )
        db.add(pago)
        db.commit()
        db.refresh(pago)
        return pago

    @staticmethod
    def update(db: Session, pago: Pago, new_estado: str, ref_externa: str = None, intentos: int = None):
        if new_estado:
            pago.estado = new_estado
        if ref_externa:
            pago.referencia_externa = ref_externa
        if intentos is not None:
            pago.intentos = intentos
            
        db.commit()
        db.refresh(pago)
        return pago

    @staticmethod
    def get_payments_to_retry(db: Session, limit_attempts: int = 3):
        """US-012: Busca pagos RECHAZADOS con intentos restantes."""
        # Se buscan pagos con estado RECHAZADO que aún no alcanzan el límite de intentos
        return db.query(Pago).filter(
            Pago.estado == "RECHAZADO",
            Pago.intentos < limit_attempts
        ).all()