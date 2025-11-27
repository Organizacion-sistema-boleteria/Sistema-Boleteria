from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.evento_schema import EventoCreate, EventoOut
from app.schemas.usuario_schema import UsuarioOut
from app.services.evento_service import EventoService
from app.core.dependencies import get_current_user, RoleChecker

# Roles permitidos para crear eventos (US-005)
PERMISOS_EVENTOS = ["ORGANIZADOR", "ADMINISTRADOR"]
check_eventos = RoleChecker(PERMISOS_EVENTOS)

evento_router = APIRouter(prefix="/api/v1/eventos", tags=["Eventos"])

# US-006: Listar Eventos Disponibles (Público)
@evento_router.get("/", status_code=status.HTTP_200_OK)
def listar_eventos(db: Session = Depends(get_db)):
    eventos = EventoService.get_all_publicos(db)
    
    return {
        "success": True,
        "message": "Eventos disponibles obtenidos exitosamente",
        "data": eventos
    }

# US-005: Crear Evento (Privado: Org/Admin)
@evento_router.post("/", status_code=status.HTTP_201_CREATED)
def crear_evento(
    data: EventoCreate, 
    db: Session = Depends(get_db), 
    current_user: UsuarioOut = Depends(get_current_user),
    rol_ok: bool = Depends(check_eventos)
):
    # Pasamos el current_user para sacar el ID del organizador
    evento = EventoService.create(db, data, current_user)
    
    return {
        "success": True,
        "message": "Evento creado exitosamente",
        "data": evento
    }