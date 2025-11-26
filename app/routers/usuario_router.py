from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate
from app.schemas.auth_schema import LoginRequest
from app.services.usuario_service import UsuarioService
from app.services.auth_service import AuthService

usuario_router = APIRouter(prefix="/api/v1/usuarios", tags=["Usuarios"])

@usuario_router.post("/", status_code=201)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = UsuarioService.create(db, data)
    
    return {
        "success": True,
        "message": "Usuario creado exitosamente",
        "data": {
            "usuarioId": usuario.usuario_id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "telefono": usuario.telefono,
            "rol": usuario.rol,
            "estado": usuario.estado,
            "fechaRegistro": usuario.fecha_registro
        }
    }

@usuario_router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return AuthService.login(db, data)

@usuario_router.get("/")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = UsuarioService.get_all(db)
    return {
        "success": True,
        "message": "Lista de usuarios obtenida correctamente",
        "data": usuarios
    }

@usuario_router.get("/{usuario_id}")
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = UsuarioService.get_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "success": True,
        "message": "Usuario obtenido correctamente",
        "data": usuario
    }

@usuario_router.put("/{usuario_id}")
def actualizar_usuario(usuario_id: int, data: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = UsuarioService.update(db, usuario_id, data)
    return {
        "success": True,
        "message": "Usuario actualizado correctamente",
        "data": usuario
    }

@usuario_router.delete("/{usuario_id}", status_code=204)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    UsuarioService.delete(db, usuario_id)
    return None
