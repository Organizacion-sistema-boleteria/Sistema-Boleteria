# app/repository/asiento_repository.py
from sqlalchemy.orm import Session
from app.domain.asiento_model import Asiento
from app.schemas.asiento_schema import AsientoCreate, AsientoUpdate


class AsientoRepository:

    @staticmethod
    def create(db: Session, data: AsientoCreate):
        asiento = Asiento(**data.dict())
        db.add(asiento)
        db.commit()
        db.refresh(asiento)
        return asiento

    @staticmethod
    def get_by_id(db: Session, asiento_id: int):
        return db.query(Asiento).filter(Asiento.asiento_id == asiento_id).first()

    @staticmethod
    def list_by_evento(db: Session, evento_id: int):
        return db.query(Asiento).filter(Asiento.evento_id == evento_id).all()

    @staticmethod
    def update(db: Session, asiento, data: AsientoUpdate):
        for field, value in data.dict(exclude_unset=True).items():
            setattr(asiento, field, value)
        db.commit()
        db.refresh(asiento)
        return asiento

    @staticmethod
    def delete(db: Session, asiento):
        db.delete(asiento)
        db.commit()
