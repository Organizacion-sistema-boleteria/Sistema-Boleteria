from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.evento_schema import EventoCreate, EventoUpdate, EventoOut
from app.services.evento_service import EventoService
from app.services.asiento_service import AsientoService

router = APIRouter(prefix="/api/v1/eventos", tags=["Eventos"])


@router.get("/", response_model=list[EventoOut])
def listar_eventos(db: Session = Depends(get_db)):
    return EventoService.get_all(db)


@router.get("/{evento_id}", response_model=EventoOut)
def obtener_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = EventoService.get_by_id(db, evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento


@router.post("/", response_model=EventoOut, status_code=201)
def crear_evento(data: EventoCreate, db: Session = Depends(get_db)):
    return EventoService.create(db, data)


@router.put("/{evento_id}", response_model=EventoOut)
def actualizar_evento(evento_id: int, data: EventoUpdate, db: Session = Depends(get_db)):
    return EventoService.update(db, evento_id, data)


@router.delete("/{evento_id}", status_code=204)
def eliminar_evento(evento_id: int, db: Session = Depends(get_db)):
    EventoService.delete(db, evento_id)
    return None


# ---- ENDPOINTS ADICIONALES ---- #

@router.get("/{evento_id}/asientos")
def obtener_asientos_evento(evento_id: int, db: Session = Depends(get_db)):
    return AsientoService.get_by_evento(db, evento_id)


@router.get("/{evento_id}/disponibilidad")
def obtener_disponibilidad(evento_id: int, db: Session = Depends(get_db)):
    return EventoService.disponibilidad(db, evento_id)
