# app/repository/pago_repository.py
from sqlalchemy.orm import Session
from app.domain.pago_model import Pago
from app.schemas.pago_schema import PagoCreate, PagoUpdate


class PagoRepository:

    @staticmethod
    def create(db: Session, data: PagoCreate):
        pago = Pago(**data.dict())
        db.add(pago)
        db.commit()
        db.refresh(pago)
        return pago

    @staticmethod
    def get_by_id(db: Session, pago_id: int):
        return db.query(Pago).filter(Pago.pago_id == pago_id).first()

    @staticmethod
    def list(db: Session):
        return db.query(Pago).all()

    @staticmethod
    def update(db: Session, pago, data: PagoUpdate):
        for field, value in data.dict(exclude_unset=True).items():
            setattr(pago, field, value)

        db.commit()
        db.refresh(pago)
        return pago

    @staticmethod
    def delete(db: Session, pago):
        db.delete(pago)
        db.commit()
