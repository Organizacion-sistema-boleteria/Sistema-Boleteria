from fastapi import APIRouter
from app.routers.usuario_router import usuario_router
from app.routers.sede_router import sede_router
from app.routers.evento_router import evento_router # <-- Nuevo router de eventos

# COMENTADO: Asientos se implementará a futuro
# from app.routers.asiento_router import asiento_router 

api_router = APIRouter()

# --- Routers Activos ---
api_router.include_router(usuario_router)
api_router.include_router(sede_router)
api_router.include_router(evento_router)

# COMENTADO: Asientos desactivado temporalmente para evitar error de importación
# api_router.include_router(asiento_router)