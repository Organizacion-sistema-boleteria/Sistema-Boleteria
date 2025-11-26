from sqlalchemy.orm import Session
from app.domain.sede_model import Sede

class SedeRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Sede).order_by(Sede.ciudad.asc(), Sede.nombre.asc()).all()

    @staticmethod
    def get_by_id(db: Session, sede_id: int):
        return db.query(Sede).filter(Sede.sede_id == sede_id).first()

    @staticmethod
    def create(db: Session, sede: Sede):
        db.add(sede)
        db.commit()
        db.refresh(sede)
        return sede

    @staticmethod
    def update(db: Session, sede: Sede):
        db.commit()
        db.refresh(sede)
        return sede

    @staticmethod
    def delete(db: Session, sede: Sede):
        db.delete(sede)
        db.commit()
