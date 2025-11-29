from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.usuario_schema import UsuarioOut
from app.schemas.pago_schema import PagoRequest
from app.services.pago_service import PagoService
from app.core.dependencies import get_current_user, RoleChecker

check_admin = RoleChecker(["ADMINISTRADOR"])
pago_router = APIRouter(prefix="/api/v1/pagos", tags=["Pagos y Boletos"])

# 1. US-011: Procesar Pago de Reserva
@pago_router.post("", status_code=status.HTTP_201_CREATED)
def procesar_pago(data: PagoRequest, db: Session = Depends(get_db), current_user: UsuarioOut = Depends(get_current_user)):
    """Procesa el pago de una reserva pendiente."""
    # La validación de rol se maneja implícitamente por get_current_user para cualquier usuario logueado.
    pago_out = PagoService.procesar_pago(db, data, current_user.usuario_id)
    return {
        "success": True,
        "message": "Pago procesado exitosamente",
        "data": pago_out
    }

# 2. US-012: Reintento Automático (Acceso de Sistema/Admin)
@pago_router.post("/reintentar", status_code=status.HTTP_200_OK)
def reintentar_pagos(db: Session = Depends(get_db), rol_ok: bool = Depends(check_admin)):
    """Desencadena la tarea de reintento para pagos fallidos con intentos restantes."""
    result = PagoService.reintentar_pagos_automatico(db)
    
    if result["total_procesados"] == 0:
        message = "No se encontraron pagos para reintentar automáticamente."
    else:
        message = f"Reintento completado: {result['aprobados']} pagos aprobados de {result['total_procesados']} reintentados."
        
    return {
        "success": True,
        "message": message,
        "data": result
    }