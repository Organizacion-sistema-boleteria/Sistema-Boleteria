# app/repository/reporte_repository.py
from sqlalchemy.orm import Session
from app.domain.reporte_model import Reporte
from app.schemas.reporte_schema import ReporteCreate, ReporteUpdate


class ReporteRepository:

    @staticmethod
    def create(db: Session, data: ReporteCreate):
        reporte = Reporte(**data.dict())
        db.add(reporte)
        db.commit()
        db.refresh(reporte)
        return reporte

    @staticmethod
    def get_by_id(db: Session, reporte_id: int):
        return db.query(Reporte).filter(Reporte.reporte_id == reporte_id).first()

    @staticmethod
    def list(db: Session):
        return db.query(Reporte).all()

    @staticmethod
    def update(db: Session, reporte, data: ReporteUpdate):
        for field, value in data.dict(exclude_unset=True).items():
            setattr(reporte, field, value)

        db.commit()
        db.refresh(reporte)
        return reporte

    @staticmethod
    def delete(db: Session, reporte):
        db.delete(reporte)
        db.commit()
