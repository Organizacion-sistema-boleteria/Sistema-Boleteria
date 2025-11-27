from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # <-- CAMBIO AQUÍ
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database import get_db
from app.domain.usuario_model import Usuario
from app.core.security import SECRET_KEY, ALGORITHM
from app.schemas.usuario_schema import UsuarioOut

# CAMBIO: Usamos HTTPBearer en lugar de OAuth2PasswordBearer
# Esto hará que Swagger muestre una caja de texto simple para pegar el token.
security = HTTPBearer()

def get_current_user(db: Session = Depends(get_db), token_auth: HTTPAuthorizationCredentials = Depends(security)) -> UsuarioOut:
    """Extrae el usuario del token JWT y verifica su existencia y estado en BD."""
    
    # CAMBIO: Extraemos el token string de las credenciales
    token = token_auth.credentials
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "success": False,
            "message": "Autenticación requerida",
            "error": {"code": 401, "details": "Token inválido o expirado"}
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("usuarioId")
        if user_id is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception

    # Buscar usuario en la base de datos
    usuario = db.query(Usuario).filter(Usuario.usuario_id == user_id).first()
    if usuario is None:
        raise credentials_exception
        
    # Validar si el usuario está activo
    if usuario.estado != "ACTIVO":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "message": "Cuenta inactiva o suspendida",
                "error": {"code": 403, "details": f"El estado del usuario es {usuario.estado}"}
            }
        )

    # Retorna el modelo de salida
    return UsuarioOut.model_validate(usuario)


class RoleChecker:
    """Clase para validar que el usuario tenga uno de los roles permitidos."""
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: UsuarioOut = Depends(get_current_user)):
        if current_user.rol not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "message": "Permisos insuficientes",
                    "error": {"code": 403, "details": f"Rol {current_user.rol} no autorizado para esta acción."}
                }
            )
        return True