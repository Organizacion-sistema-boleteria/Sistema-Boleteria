# app/repository/usuario_repository.py
from sqlalchemy.orm import Session
from app.domain.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate


class UsuarioRepository:

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(Usuario).filter(Usuario.email == email).first()

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.query(Usuario).filter(Usuario.usuario_id == user_id).first()

    @staticmethod
    def list(db: Session):
        return db.query(Usuario).all()

    @staticmethod
    def create(db: Session, data: UsuarioCreate):
        usuario = Usuario(
            nombre=data.nombre,
            email=data.email,
            telefono=data.telefono,
            password_hash=data.password,  # <── conversión correcta
            rol=data.rol,
            estado=data.estado
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def update(db: Session, usuario: Usuario, data: UsuarioUpdate):
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(usuario, key, value)
        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def delete(db: Session, usuario: Usuario):
        db.delete(usuario)
        db.commit()
