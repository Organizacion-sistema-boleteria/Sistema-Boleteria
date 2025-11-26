from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.asiento_schema import AsientoCreate, AsientoUpdate, AsientoOut
from app.services.asiento_service import AsientoService

router = APIRouter(prefix="/api/v1/asientos", tags=["Asientos"])


@router.get("/", response_model=list[AsientoOut])
def listar_asientos(db: Session = Depends(get_db)):
    return AsientoService.get_all(db)


@router.get("/{asiento_id}", response_model=AsientoOut)
def obtener_asiento(asiento_id: int, db: Session = Depends(get_db)):
    asiento = AsientoService.get_by_id(db, asiento_id)
    if not asiento:
        raise HTTPException(status_code=404, detail="Asiento no encontrado")
    return asiento


@router.post("/", response_model=AsientoOut, status_code=201)
def crear_asiento(data: AsientoCreate, db: Session = Depends(get_db)):
    return AsientoService.create(db, data)


@router.put("/{asiento_id}", response_model=AsientoOut)
def actualizar_asiento(asiento_id: int, data: AsientoUpdate, db: Session = Depends(get_db)):
    return AsientoService.update(db, asiento_id, data)


@router.delete("/{asiento_id}", status_code=204)
def eliminar_asiento(asiento_id: int, db: Session = Depends(get_db)):
    AsientoService.delete(db, asiento_id)
    return None
