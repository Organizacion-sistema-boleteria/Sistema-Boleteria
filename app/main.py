from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

# Importar el enrutador que agrupa todas las rutas del sistema
from app.config.routers import api_router

# Cargar variables del archivo .env
load_dotenv()

# Obtener valores desde las variables de entorno
APP_NAME = os.getenv("APP_NAME", "Sistema de Boletería")
DEBUG = os.getenv("DEBUG", "True")
SECRET_KEY = os.getenv("SECRET_KEY", "clave_por_defecto")

# Crear la instancia de FastAPI
app = FastAPI(
    title=APP_NAME,
    description="API RESTful del Sistema de Boletería",
    version="1.0.0",
    debug=DEBUG.lower() == "true"
)

# Incluir todos los routers reales (usuarios, sedes, eventos, pagos, etc.)
app.include_router(api_router)

# Ruta raíz
@app.get("/")
async def root():
    return {
        "message": f"¡Bienvenido a {APP_NAME}!",
        "status": "online",
        "version": "1.0.0",
        "debug_mode": DEBUG
    }

# Health check
@app.get("/health")
async def health_check():
    return JSONResponse(
        status_code=200,
        content={"status": "healthy"}
    )
