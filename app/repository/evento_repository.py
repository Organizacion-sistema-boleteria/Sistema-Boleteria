# app/repository/evento_repository.py
from sqlalchemy.orm import Session
from app.domain.evento_model import Evento
from app.schemas.evento_schema import EventoCreate, EventoUpdate

class EventoRepository:

    @staticmethod
    def create(db: Session, data: EventoCreate) -> Evento:
        evento = Evento(
            sede_id=data.sede_id,
            organizador_id=data.organizador_id,
            titulo=data.titulo,
            descripcion=data.descripcion,
            fecha_evento=data.fecha_evento,
            fecha_venta_inicio=data.fecha_venta_inicio,
            fecha_venta_fin=data.fecha_venta_fin,
            precio_base=data.precio_base,
            categoria=data.categoria,
        )
        db.add(evento)
        db.commit()
        db.refresh(evento)
        return evento

    @staticmethod
    def get_by_id(db: Session, evento_id: int) -> Evento | None:
        return db.query(Evento).filter(Evento.evento_id == evento_id).first()

    @staticmethod
    def list(db: Session):
        return db.query(Evento).all()

    @staticmethod
    def update(db: Session, evento: Evento, data: EventoUpdate) -> Evento:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(evento, field, value)

        db.commit()
        db.refresh(evento)
        return evento

    @staticmethod
    def delete(db: Session, evento: Evento):
        db.delete(evento)
        db.commit()
