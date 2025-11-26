from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.domain.sede_model import Sede
from app.repository.sede_repository import SedeRepository

class SedeService:

    @staticmethod
    def get_all(db: Session):
        return SedeRepository.get_all(db)

    @staticmethod
    def get_by_id(db: Session, sede_id: int):
        return SedeRepository.get_by_id(db, sede_id)

    @staticmethod
    def create(db: Session, data):
        if data.capacidad_total <= 0:
            raise HTTPException(status_code=400, detail="La capacidad total debe ser mayor a 0")

        new_sede = Sede(
            nombre=data.nombre,
            direccion=data.direccion,
            ciudad=data.ciudad,
            capacidad_total=data.capacidad_total,
            descripcion=data.descripcion,
            estado="ACTIVA"
        )

        return SedeRepository.create(db, new_sede)

    @staticmethod
    def update(db: Session, sede_id: int, data):
        sede = SedeRepository.get_by_id(db, sede_id)
        if not sede:
            raise HTTPException(status_code=404, detail="Sede no encontrada")

        updates = data.dict(exclude_unset=True, by_alias=False)

        for field, value in updates.items():
            setattr(sede, field, value)

        return SedeRepository.update(db, sede)

    @staticmethod
    def delete(db: Session, sede_id: int):
        sede = SedeRepository.get_by_id(db, sede_id)
        if not sede:
            raise HTTPException(status_code=404, detail="Sede no encontrada")

        SedeRepository.delete(db, sede)
        return True
