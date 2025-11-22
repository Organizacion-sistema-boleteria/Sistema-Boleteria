# app/repository/sede_repository.py
from sqlalchemy.orm import Session
from app.domain.sede_model import Sede
from app.schemas.sede_schema import SedeCreate, SedeUpdate

class SedeRepository:

    @staticmethod
    def create(db: Session, data: SedeCreate) -> Sede:
        sede = Sede(
            nombre=data.nombre,
            direccion=data.direccion,
            ciudad=data.ciudad,
            capacidad_total=data.capacidad_total,
            descripcion=data.descripcion,
        )
        db.add(sede)
        db.commit()
        db.refresh(sede)
        return sede

    @staticmethod
    def get_by_id(db: Session, sede_id: int) -> Sede | None:
        return db.query(Sede).filter(Sede.sede_id == sede_id).first()

    @staticmethod
    def list(db: Session):
        return db.query(Sede).all()

    @staticmethod
    def update(db: Session, sede: Sede, data: SedeUpdate) -> Sede:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(sede, field, value)

        db.commit()
        db.refresh(sede)
        return sede

    @staticmethod
    def delete(db: Session, sede: Sede):
        db.delete(sede)
        db.commit()
