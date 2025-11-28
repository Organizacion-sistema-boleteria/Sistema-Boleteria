from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.asiento_schema import AsientosCreateRequest, AsientoUpdate, AsientoOut
from app.schemas.usuario_schema import UsuarioOut
from app.services.asiento_service import AsientoService
from app.core.dependencies import get_current_user, RoleChecker

check_permisos = RoleChecker(["ORGANIZADOR", "ADMINISTRADOR"])
asiento_router = APIRouter(tags=["Asientos"])

@asiento_router.post("/api/v1/eventos/{evento_id}/asientos", status_code=201)
def crear_asientos(evento_id: int, data: AsientosCreateRequest, db: Session = Depends(get_db), u: UsuarioOut = Depends(get_current_user), ok: bool = Depends(check_permisos)):
    res = AsientoService.crear_asientos_masivos(db, evento_id, data, u)
    return {"success": True, "message": "Asientos creados", "data": res}

@asiento_router.get("/api/v1/eventos/{evento_id}/asientos")
def listar_asientos(evento_id: int, db: Session = Depends(get_db)):
    res = AsientoService.consultar_disponibilidad(db, evento_id)
    return {"success": True, "message": "Disponibilidad obtenida", "data": res}

@asiento_router.put("/api/v1/asientos/{id}")
def actualizar(id: int, data: AsientoUpdate, db: Session = Depends(get_db), u: UsuarioOut = Depends(get_current_user), ok: bool = Depends(check_permisos)):
    res = AsientoService.update(db, id, data)
    return {"success": True, "message": "Actualizado", "data": res}

@asiento_router.delete("/api/v1/asientos/{id}")
def eliminar(id: int, db: Session = Depends(get_db), u: UsuarioOut = Depends(get_current_user), ok: bool = Depends(check_permisos)):
    AsientoService.delete(db, id)
    return {"success": True, "message": "Eliminado", "data": None}