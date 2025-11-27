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
    def create(db: Session, data: UsuarioCreate, password_hash: str):
        usuario = Usuario(
            nombre=data.nombre,
            email=data.email,
            telefono=data.telefono,
            password_hash=password_hash,
            # Usa el rol que viene del servicio (que ya fue validado o forzado a CLIENTE)
            rol=data.rol, 
            estado="ACTIVO",
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def update(db: Session, usuario: Usuario, data: UsuarioUpdate):
        for key, value in data.model_dump(exclude_unset=True).items():

            if key == "password":
                continue

            setattr(usuario, key, value)

        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def delete(db: Session, usuario: Usuario):
        db.delete(usuario)
        db.commit()