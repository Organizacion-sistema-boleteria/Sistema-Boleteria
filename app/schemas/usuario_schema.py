from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    estado: str = "ACTIVO"


class UsuarioCreate(UsuarioBase):
    password: str
    rol: str = "CLIENTE"

    @field_validator("password")
    def validar_password(cls, v: str):
        if len(v) < 8:
            raise ValueError("La contraseña es demasiado corta")
        return v


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    password: Optional[str] = None
    rol: Optional[str] = None
    estado: Optional[str] = None


class UsuarioOut(BaseModel):
    usuario_id: int
    nombre: str
    email: str
    telefono: Optional[str]
    rol: str
    estado: str
    fecha_registro: datetime

    class Config:
        from_attributes = True
