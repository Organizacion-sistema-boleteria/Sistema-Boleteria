from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Obtener valores desde las variables de entorno
APP_NAME = os.getenv("APP_NAME", "Mi API con FastAPI")
DEBUG = os.getenv("DEBUG", "True")
SECRET_KEY = os.getenv("SECRET_KEY", "clave_por_defecto")

# Crear la instancia de FastAPI
app = FastAPI(
    title=APP_NAME,
    description="API RESTful profesional",
    version="1.0.0",
    debug=DEBUG.lower() == "true"
)

# Ruta raíz
@app.get("/")
async def root():
    """
    Endpoint de bienvenida.
    """
    return {
        "message": f"¡Bienvenido a {APP_NAME}!",
        "status": "online",
        "version": "1.0.0",
        "debug_mode": DEBUG
    }

# Endpoint con parámetros
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    """
    Ejemplo con parámetros de ruta y query.
    """
    return {
        "item_id": item_id,
        "query": q
    }

# Health check
@app.get("/health")
async def health_check():
    """
    Verifica el estado del servidor.
    """
    return JSONResponse(
        status_code=200,
        content={"status": "healthy"}
    )
