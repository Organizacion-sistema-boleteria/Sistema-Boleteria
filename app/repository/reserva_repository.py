# app/repository/reserva_repository.py
from sqlalchemy.orm import Session
from app.domain.reserva_model import Reserva, Reserva_Asiento
from app.schemas.reserva_schema import ReservaCreate, ReservaUpdate
from app.domain.asiento_model import Asiento


class ReservaRepository:

    @staticmethod
    def create(db: Session, data: ReservaCreate):
        reserva = Reserva(
            usuario_id=data.usuario_id,
            evento_id=data.evento_id,
            fecha_expiracion=data.fecha_expiracion,
            estado=data.estado,
            precio_total=data.precio_total
        )

        db.add(reserva)
        db.commit()
        db.refresh(reserva)

        # Registrar relación N:M
        for asiento_id in data.asientos_ids:
            db.execute(
                Reserva_Asiento.insert().values(
                    reserva_id=reserva.reserva_id,
                    asiento_id=asiento_id
                )
            )

        db.commit()
        return reserva

    @staticmethod
    def get_by_id(db: Session, reserva_id: int):
        return (
            db.query(Reserva)
            .filter(Reserva.reserva_id == reserva_id)
            .first()
        )

    @staticmethod
    def list(db: Session):
        return db.query(Reserva).all()

    @staticmethod
    def update(db: Session, reserva, data: ReservaUpdate):
        for field, value in data.dict(exclude_unset=True).items():
            if field == "asientos_ids":
                db.execute(
                    Reserva_Asiento.delete().where(
                        Reserva_Asiento.c.reserva_id == reserva.reserva_id
                    )
                )
                for asiento_id in value:
                    db.execute(
                        Reserva_Asiento.insert().values(
                            reserva_id=reserva.reserva_id,
                            asiento_id=asiento_id
                        )
                    )
            else:
                setattr(reserva, field, value)

        db.commit()
        db.refresh(reserva)
        return reserva

    @staticmethod
    def delete(db: Session, reserva):
        db.execute(
            Reserva_Asiento.delete().where(
                Reserva_Asiento.c.reserva_id == reserva.reserva_id
            )
        )

        db.delete(reserva)
        db.commit()
