from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repository.usuario_repository import UsuarioRepository
from app.schemas.auth_schema import LoginRequest
from app.core.security import verify_password, create_access_token


class AuthService:

    @staticmethod
    def login(db: Session, data: LoginRequest):
        usuario = UsuarioRepository.get_by_email(db, data.email)

        # Usuario no encontrado
        if not usuario:
            raise HTTPException(
                status_code=401,
                detail={
                    "success": False,
                    "message": "Credenciales inválidas",
                    "error": {
                        "code": 401,
                        "details": "Email o contraseña incorrectos"
                    }
                }
            )

        # Contraseña incorrecta
        if not verify_password(data.password, usuario.password_hash):
            raise HTTPException(
                status_code=401,
                detail={
                    "success": False,
                    "message": "Credenciales inválidas",
                    "error": {
                        "code": 401,
                        "details": "Email o contraseña incorrectos"
                    }
                }
            )

        # Estado del usuario
        if usuario.estado != "ACTIVO":
            raise HTTPException(
                status_code=403,
                detail={
                    "success": False,
                    "message": "Cuenta inactiva o suspendida",
                    "error": {
                        "code": 403,
                        "details": f"El usuario está en estado {usuario.estado}"
                    }
                }
            )

        # Token
        token = create_access_token({
            "usuarioId": usuario.usuario_id,
            "rol": usuario.rol
        })

        return {
            "success": True,
            "message": "Inicio de sesión exitoso",
            "data": {
                "usuarioId": usuario.usuario_id,
                "nombre": usuario.nombre,
                "email": usuario.email,
                "rol": usuario.rol,
                "token": token
            }
        }
