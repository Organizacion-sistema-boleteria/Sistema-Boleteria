from fastapi import APIRouter
from app.api.evento_api import router as evento_api

evento_router = APIRouter()
evento_router.include_router(evento_api)
