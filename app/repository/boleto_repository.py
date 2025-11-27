# app/repository/boleto_repository.py
from sqlalchemy.orm import Session
from app.domain.boleto_model import Boleto
from app.schemas.boleto_schema import BoletoCreate, BoletoUpdate


class BoletoRepository:

    @staticmethod
    def create(db: Session, data: BoletoCreate):
        boleto = Boleto(**data.dict())
        db.add(boleto)
        db.commit()
        db.refresh(boleto)
        return boleto

    @staticmethod
    def get_by_id(db: Session, boleto_id: int):
        return db.query(Boleto).filter(Boleto.boleto_id == boleto_id).first()

    @staticmethod
    def list(db: Session):
        return db.query(Boleto).all()

    @staticmethod
    def list_by_pago(db: Session, pago_id: int):
        return db.query(Boleto).filter(Boleto.pago_id == pago_id).all()

    @staticmethod
    def update(db: Session, boleto, data: BoletoUpdate):
        for field, value in data.dict(exclude_unset=True).items():
            setattr(boleto, field, value)

        db.commit()
        db.refresh(boleto)
        return boleto

    @staticmethod
    def delete(db: Session, boleto):
        db.delete(boleto)
        db.commit()
