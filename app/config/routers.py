from fastapi import APIRouter
from app.routers.usuario_router import usuario_router
from app.routers.sede_router import sede_router
from app.routers.evento_router import evento_router
from app.routers.asiento_router import asiento_router
from app.routers.reserva_router import reserva_router 

api_router = APIRouter()

api_router.include_router(usuario_router)
api_router.include_router(sede_router)
api_router.include_router(evento_router)
api_router.include_router(asiento_router)
api_router.include_router(reserva_router)