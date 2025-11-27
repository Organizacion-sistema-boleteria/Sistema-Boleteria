from fastapi import APIRouter
from app.api.asiento_api import router as asiento_api

asiento_router = APIRouter()
asiento_router.include_router(asiento_api)
