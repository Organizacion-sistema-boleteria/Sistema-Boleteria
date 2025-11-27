from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.evento_schema import EventoCreate, EventoOut, EventoUpdate
from app.schemas.usuario_schema import UsuarioOut
from app.services.evento_service import EventoService
from app.core.dependencies import get_current_user, RoleChecker

# --- PERMISOS ---
# Crear y Editar: Organizadores y Admins
PERMISOS_GESTION = ["ORGANIZADOR", "ADMINISTRADOR"]
check_gestion = RoleChecker(PERMISOS_GESTION)

# Eliminar: Solo Admins
PERMISOS_ADMIN = ["ADMINISTRADOR"]
check_admin = RoleChecker(PERMISOS_ADMIN)

evento_router = APIRouter(prefix="/api/v1/eventos", tags=["Eventos"])


# 1. LISTAR EVENTOS (Público) - [US-006]
@evento_router.get("/", status_code=status.HTTP_200_OK)
def listar_eventos(db: Session = Depends(get_db)):
    eventos = EventoService.get_all_publicos(db)
    return {
        "success": True,
        "message": "Eventos disponibles obtenidos",
        "data": eventos
    }

# 2. CREAR EVENTO (Privado: Org/Admin) - [US-005]
@evento_router.post("/", status_code=status.HTTP_201_CREATED)
def crear_evento(
    data: EventoCreate, 
    db: Session = Depends(get_db), 
    current_user: UsuarioOut = Depends(get_current_user),
    rol_ok: bool = Depends(check_gestion)
):
    evento = EventoService.create(db, data, current_user)
    return {
        "success": True,
        "message": "Evento creado exitosamente",
        "data": evento
    }

# 3. CONSULTAR DETALLE EVENTO (Público)
@evento_router.get("/{evento_id}", status_code=status.HTTP_200_OK)
def consultar_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = EventoService.get_by_id(db, evento_id)
    return {
        "success": True,
        "message": "Evento encontrado",
        "data": evento
    }

# 4. ACTUALIZAR EVENTO (Privado: Org/Admin)
@evento_router.put("/{evento_id}", status_code=status.HTTP_200_OK)
def actualizar_evento(
    evento_id: int,
    data: EventoUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioOut = Depends(get_current_user),
    rol_ok: bool = Depends(check_gestion)
):
    evento = EventoService.update(db, evento_id, data, current_user)
    return {
        "success": True,
        "message": "Evento actualizado exitosamente",
        "data": evento
    }

# 5. ELIMINAR EVENTO (Privado: Solo Admin)
@evento_router.delete("/{evento_id}", status_code=status.HTTP_200_OK)
def eliminar_evento(
    evento_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioOut = Depends(get_current_user),
    rol_ok: bool = Depends(check_admin)
):
    EventoService.delete(db, evento_id)
    return {
        "success": True,
        "message": "Evento eliminado exitosamente",
        "data": None
    }