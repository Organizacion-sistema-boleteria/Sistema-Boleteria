from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.sede_schema import SedeCreate, SedeUpdate, SedeOut
from app.schemas.usuario_schema import UsuarioOut
from app.services.sede_service import SedeService
from app.core.dependencies import get_current_user, RoleChecker

# --- DEFINICIÓN DE PERMISOS ---
PERMISOS_GESTION = ["ORGANIZADOR", "ADMINISTRADOR"]
check_gestion = RoleChecker(PERMISOS_GESTION)

PERMISOS_ADMIN = ["ADMINISTRADOR"]
check_admin = RoleChecker(PERMISOS_ADMIN)

sede_router = APIRouter(prefix="/api/v1/sedes", tags=["Sedes"])


# 1. LISTAR SEDES (Público)
# CORRECCIÓN: Quitamos 'response_model=List[SedeOut]' para permitir devolver el objeto {success, data}
@sede_router.get("/", status_code=status.HTTP_200_OK)
def listar_sedes(db: Session = Depends(get_db)):
    sedes = SedeService.get_all(db)
    
    return {
        "success": True,
        "message": "Sedes obtenidas exitosamente",
        "data": sedes
    }

# 2. CREAR SEDE (Privado: Organizador/Admin)
@sede_router.post("/", status_code=status.HTTP_201_CREATED)
def crear_sede(
    data: SedeCreate, 
    db: Session = Depends(get_db), 
    current_user: UsuarioOut = Depends(get_current_user),
    rol_ok: bool = Depends(check_gestion)
):
    sede = SedeService.create(db, data)
    return {
        "success": True,
        "message": "Sede creada exitosamente",
        "data": sede
    }

# 3. CONSULTAR DETALLE SEDE (Público)
@sede_router.get("/{sede_id}", status_code=status.HTTP_200_OK)
def consultar_sede(sede_id: int, db: Session = Depends(get_db)):
    sede = SedeService.get_by_id(db, sede_id)
    return {
        "success": True,
        "message": "Sede encontrada",
        "data": sede
    }

# 4. ACTUALIZAR SEDE (Privado: Organizador/Admin)
@sede_router.put("/{sede_id}", status_code=status.HTTP_200_OK)
def actualizar_sede(
    sede_id: int, 
    data: SedeUpdate, 
    db: Session = Depends(get_db),
    current_user: UsuarioOut = Depends(get_current_user),
    rol_ok: bool = Depends(check_gestion)
):
    sede = SedeService.update(db, sede_id, data)
    return {
        "success": True,
        "message": "Sede actualizada exitosamente",
        "data": sede
    }

# 5. ELIMINAR/DESHABILITAR SEDE (Privado: Solo Admin)
@sede_router.delete("/{sede_id}", status_code=status.HTTP_200_OK)
def eliminar_sede(
    sede_id: int, 
    db: Session = Depends(get_db),
    current_user: UsuarioOut = Depends(get_current_user),
    rol_ok: bool = Depends(check_admin)
):
    SedeService.delete(db, sede_id)
    return {
        "success": True,
        "message": "Sede eliminada exitosamente",
        "data": None
    }