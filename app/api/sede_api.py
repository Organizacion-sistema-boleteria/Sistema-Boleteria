from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.sede_schema import SedeCreate, SedeUpdate, SedeOut
from app.services.sede_service import SedeService

router = APIRouter(prefix="/api/v1/sedes", tags=["Sedes"])


@router.get("/", response_model=list[SedeOut])
def listar_sedes(db: Session = Depends(get_db)):
    return SedeService.get_all(db)


@router.get("/{sede_id}", response_model=SedeOut)
def obtener_sede(sede_id: int, db: Session = Depends(get_db)):
    sede = SedeService.get_by_id(db, sede_id)
    if not sede:
        raise HTTPException(status_code=404, detail="Sede no encontrada")
    return sede


@router.post("/", response_model=SedeOut, status_code=201)
def crear_sede(data: SedeCreate, db: Session = Depends(get_db)):
    return SedeService.create(db, data)


@router.put("/{sede_id}", response_model=SedeOut)
def actualizar_sede(sede_id: int, data: SedeUpdate, db: Session = Depends(get_db)):
    return SedeService.update(db, sede_id, data)


@router.delete("/{sede_id}", status_code=204)
def eliminar_sede(sede_id: int, db: Session = Depends(get_db)):
    SedeService.delete(db, sede_id)
    return None
