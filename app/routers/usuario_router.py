from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioOut
from app.schemas.auth_schema import LoginRequest
from app.services.usuario_service import UsuarioService
from app.services.auth_service import AuthService
from app.core.dependencies import get_current_user, RoleChecker

# Roles permitidos para crear usuarios especiales (solo ADMIN)
ALLOWED_ROLES_ADMIN_CREATE = ["ADMINISTRADOR"]
has_admin_role = RoleChecker(ALLOWED_ROLES_ADMIN_CREATE)

usuario_router = APIRouter(prefix="/api/v1/usuarios", tags=["Usuarios"])


# US-001: Registro público (crea solo CLIENTES)
@usuario_router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = UsuarioService.create(db, data, is_admin_context=False)

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


# Crear usuario con Rol (solo ADMIN)
@usuario_router.post("/admin-create", status_code=status.HTTP_201_CREATED, response_model=None)
def crear_usuario_con_rol(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioOut = Depends(get_current_user),
    roles_ok: bool = Depends(has_admin_role)
):
    usuario = UsuarioService.create(db, data, is_admin_context=True)

    return {
        "success": True,
        "message": "Usuario creado con rol específico exitosamente",
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


# US-002: Login
@usuario_router.post("/login", response_model=None)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return AuthService.login(db, data)


# Listar usuarios
@usuario_router.get("/", response_model=None)
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = UsuarioService.get_all(db)
    return {
        "success": True,
        "message": "Lista de usuarios obtenida correctamente",
        "data": usuarios
    }


# Obtener usuario por ID
@usuario_router.get("/{usuario_id}", response_model=None)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = UsuarioService.get_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return {
        "success": True,
        "message": "Usuario obtenido correctamente",
        "data": usuario
    }


# Actualizar usuario
@usuario_router.put("/{usuario_id}", response_model=None)
def actualizar_usuario(usuario_id: int, data: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = UsuarioService.update(db, usuario_id, data)
    return {
        "success": True,
        "message": "Usuario actualizado correctamente",
        "data": usuario
    }


# Eliminar usuario
@usuario_router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    UsuarioService.delete(db, usuario_id)
    return None
