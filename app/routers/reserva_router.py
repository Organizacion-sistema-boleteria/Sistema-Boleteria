from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.reserva_schema import ReservaCreateRequest, ReservaResponse, ReservaListResponse, ExpiracionResponse
from app.services.reserva_service import ReservaService
from app.schemas.usuario_schema import UsuarioOut
from app.core.dependencies import get_current_user, RoleChecker

# Roles
# NOTA: check_cliente solo permite usuarios con rol "CLIENTE"
check_cliente = RoleChecker(["CLIENTE"])
check_admin = RoleChecker(["ADMINISTRADOR"])
check_organizador_admin = RoleChecker(["ADMINISTRADOR", "ORGANIZADOR"])

reserva_router = APIRouter(tags=["Reservas"])

# 1. Crear Reserva (US-009) - HABILITADO PARA ROL CLIENTE
# Este endpoint SOLO requiere el rol CLIENTE, como indican las historias de usuario.
@reserva_router.post("/api/v1/reservas", status_code=status.HTTP_201_CREATED)
def crear_reserva(
    data: ReservaCreateRequest, 
    db: Session = Depends(get_db), 
    u: UsuarioOut = Depends(get_current_user), 
    ok: bool = Depends(check_cliente) # <--- ¡Aquí está la verificación del rol CLIENTE!
):
    res = ReservaService.crear_reserva(db, data, u.usuario_id)
    if not res["success"]:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=res)
    return res

# 2. Cancelar Expiradas (US-010) - Protegido por Admin (Tarea de mantenimiento)
@reserva_router.delete("/api/v1/reservas/expiradas", response_model=ExpiracionResponse)
def cancelar_expiradas(db: Session = Depends(get_db), u: UsuarioOut = Depends(get_current_user), ok: bool = Depends(check_admin)):
    return ReservaService.cancelar_reservas_expiradas(db)

# 3. Listar Mis Reservas
@reserva_router.get("/api/v1/reservas/me")
def mis_reservas(
    db: Session = Depends(get_db), 
    u: UsuarioOut = Depends(get_current_user),
    ok: bool = Depends(check_cliente) # Solo clientes pueden ver sus propias reservas
):
    data = ReservaService.obtener_por_usuario(db, u.usuario_id)
    return {"success": True, "message": "Reservas obtenidas", "data": data}

# 4. Obtener Detalle de una Reserva
@reserva_router.get("/api/v1/reservas/{id}")
def detalle_reserva(
    id: int, 
    db: Session = Depends(get_db), 
    u: UsuarioOut = Depends(get_current_user)
):
    # La validación de si es dueño o administrador está dentro del servicio
    data = ReservaService.obtener_detalle(db, id, u.usuario_id, u.rol in ["ADMINISTRADOR", "ORGANIZADOR"])
    return {"success": True, "message": "Detalle obtenido", "data": data}

# 5. Cancelar Reserva Manualmente
@reserva_router.put("/api/v1/reservas/{id}/cancelar")
def cancelar_manual(
    id: int, 
    db: Session = Depends(get_db), 
    u: UsuarioOut = Depends(get_current_user)
):
    # La validación de que solo el dueño puede cancelar está dentro del servicio
    return ReservaService.cancelar_manual(db, id, u.usuario_id)