from sqlalchemy.orm import Session
from sqlalchemy import asc
from app.domain.evento_model import Evento
from app.schemas.evento_schema import EventoCreate, EventoUpdate

class EventoRepository:

    @staticmethod
    def get_by_id(db: Session, evento_id: int):
        return db.query(Evento).filter(Evento.evento_id == evento_id).first()

    @staticmethod
    def list_all(db: Session):
        return db.query(Evento).all()

    @staticmethod
    def list_by_estado(db: Session, estado: str):
        # US-006: Filtrar por estado y ordenar por fecha (próximos primero)
        return db.query(Evento).filter(Evento.estado == estado).order_by(asc(Evento.fecha_evento)).all()

    @staticmethod
    def create(db: Session, data: EventoCreate, organizador_id: int):
        # Creamos el objeto modelo usando los datos del schema
        evento_dict = data.model_dump()
        evento = Evento(**evento_dict)
        # Asignamos explícitamente el organizador que viene del token
        evento.organizador_id = organizador_id 
        
        db.add(evento)
        db.commit()
        db.refresh(evento)
        return evento

    @staticmethod
    def update(db: Session, evento: Evento, data: EventoUpdate):
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(evento, key, value)

        db.commit()
        db.refresh(evento)
        return evento

    @staticmethod
    def delete(db: Session, evento: Evento):
        db.delete(evento)
        db.commit()