from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.sede_schema import SedeCreate, SedeUpdate, SedeOut
from app.services.sede_service import SedeService

sede_router = APIRouter(
    prefix="/api/v1/sedes",
    tags=["Sedes"]
)

@sede_router.get("/", response_model=list[SedeOut])
def listar_sedes(db: Session = Depends(get_db)):
    """
    Devuelve una lista con todas las sedes registradas.
    """
    return SedeService.get_all(db)

@sede_router.get("/{sede_id}", response_model=SedeOut)
def obtener_sede(sede_id: int, db: Session = Depends(get_db)):
    """
    Obtiene la información de una sede por su ID.
    """
    sede = SedeService.get_by_id(db, sede_id)
    if not sede:
        raise HTTPException(status_code=404, detail="Sede no encontrada")
    return sede

@sede_router.post("/", response_model=SedeOut, status_code=201)
def crear_sede(data: SedeCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva sede con los datos enviados en el cuerpo de la petición.
    """
    return SedeService.create(db, data)

@sede_router.put("/{sede_id}", response_model=SedeOut)
def actualizar_sede(sede_id: int, data: SedeUpdate, db: Session = Depends(get_db)):
    """
    Actualiza la información de una sede existente.
    """
    sede = SedeService.update(db, sede_id, data)
    if not sede:
        raise HTTPException(status_code=404, detail="Sede no encontrada")
    return sede

@sede_router.delete("/{sede_id}", status_code=204)
def eliminar_sede(sede_id: int, db: Session = Depends(get_db)):
    """
    Elimina una sede por su ID.
    """
    eliminado = SedeService.delete(db, sede_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Sede no encontrada")
    return None
