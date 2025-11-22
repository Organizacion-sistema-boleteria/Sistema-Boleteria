from pydantic import BaseModel, EmailStr
from typing import Optional


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    rol: str
    estado: str


class UsuarioCreate(UsuarioBase):
    password: str  # <── ESTE ES EL CAMPO OBLIGATORIO QUE FALTABA


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    rol: Optional[str] = None
    estado: Optional[str] = None


class UsuarioOut(UsuarioBase):
    usuario_id: int

    model_config = {
        "from_attributes": True
    }
