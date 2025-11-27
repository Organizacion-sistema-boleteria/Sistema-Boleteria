from sqlalchemy.orm import Session
from sqlalchemy import asc
from app.domain.sede_model import Sede
from app.schemas.sede_schema import SedeCreate, SedeUpdate

class SedeRepository:

    @staticmethod
    def get_by_id(db: Session, sede_id: int):
        return db.query(Sede).filter(Sede.sede_id == sede_id).first()

    @staticmethod
    def list(db: Session):
        # Ordenar por ciudad y nombre
        return db.query(Sede).order_by(asc(Sede.ciudad), asc(Sede.nombre)).all()

    @staticmethod
    def create(db: Session, data: SedeCreate):
        sede = Sede(
            nombre=data.nombre,
            direccion=data.direccion,
            ciudad=data.ciudad,
            capacidad_total=data.capacidad_total,
            descripcion=data.descripcion,
            estado="ACTIVA", 
        )
        db.add(sede)
        db.commit()
        db.refresh(sede)
        return sede

    @staticmethod
    def update(db: Session, sede: Sede, data: SedeUpdate):
        # Actualiza solo los campos que vienen en el request
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(sede, key, value)

        db.commit()
        db.refresh(sede)
        return sede

    @staticmethod
    def delete(db: Session, sede: Sede):
        db.delete(sede)
        db.commit()