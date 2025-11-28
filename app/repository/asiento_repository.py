from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.domain.asiento_model import Asiento
from app.schemas.asiento_schema import AsientoUpdate

class AsientoRepository:
    @staticmethod
    def create_bulk(db: Session, asientos: List[Asiento]):
        db.add_all(asientos)
        db.commit()
        return len(asientos)

    @staticmethod
    def get_by_evento(db: Session, e_id: int):
        return db.query(Asiento).filter(Asiento.evento_id == e_id).order_by(Asiento.seccion, Asiento.fila, Asiento.numero).all()

    @staticmethod
    def count_by_evento(db: Session, e_id: int):
        return db.query(func.count(Asiento.asiento_id)).filter(Asiento.evento_id == e_id).scalar()

    @staticmethod
    def get_by_id(db: Session, id: int):
        return db.query(Asiento).filter(Asiento.asiento_id == id).first()

    @staticmethod
    def update(db: Session, asiento: Asiento, data: AsientoUpdate):
        for k, v in data.model_dump(exclude_unset=True).items(): setattr(asiento, k, v)
        db.commit(); db.refresh(asiento)
        return asiento

    @staticmethod
    def delete(db: Session, asiento: Asiento):
        db.delete(asiento); db.commit()