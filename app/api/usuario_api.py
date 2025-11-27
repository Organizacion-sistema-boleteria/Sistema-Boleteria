from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioOut
from app.services.usuario_service import UsuarioService

router = APIRouter(prefix="/api/v1/usuarios", tags=["Usuarios"])


@router.post("/", status_code=201)
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


@router.get("/")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = UsuarioService.get_all(db)

    return {
        "success": True,
        "message": "Listado de usuarios",
        "data": usuarios
    }


@router.get("/{usuario_id}")
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = UsuarioService.get_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "success": True,
        "message": "Usuario encontrado",
        "data": usuario
    }


@router.put("/{usuario_id}")
def actualizar_usuario(usuario_id: int, data: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = UsuarioService.update(db, usuario_id, data)

    return {
        "success": True,
        "message": "Usuario actualizado exitosamente",
        "data": usuario
    }


@router.delete("/{usuario_id}", status_code=204)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    UsuarioService.delete(db, usuario_id)
    return None
