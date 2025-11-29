from sqlalchemy.orm import Session
from app.domain.reserva_model import Reserva
from app.domain.asiento_model import Asiento
from typing import List
from datetime import datetime, timedelta
from sqlalchemy import text

class ReservaRepository:
    
    @staticmethod
    def crear(db: Session, reserva: Reserva):
        db.add(reserva)
        # Se debe llamar db.flush() en el servicio para obtener el ID antes de actualizar asientos
        return reserva

    @staticmethod
    def get_by_id(db: Session, reserva_id: int) -> Reserva:
        return db.query(Reserva).filter(Reserva.reserva_id == reserva_id).first()

    @staticmethod
    def obtener_pendientes_expiradas(db: Session) -> List[Reserva]:
        """Obtiene reservas pendientes cuya fecha de expiración ya pasó."""
        # Se calcula el tiempo en la base de datos para manejar la zona horaria (aunque en SQLite no es estricto, es buena práctica)
        # Aquí usamos la lógica del servicio para la hora actual:
        ahora = datetime.utcnow() - timedelta(seconds=1) # Pequeño margen
        
        return db.query(Reserva).filter(
            Reserva.estado == "PENDIENTE",
            Reserva.fecha_expiracion < ahora
        ).all()

    @staticmethod
    def get_asientos_by_ids_lock(db: Session, ids: List[int], evento_id: int) -> List[Asiento]:
        """Obtiene asientos por ID y los bloquea para asegurar atomicidad."""
        # SQLite no soporta nativamente FOR UPDATE, pero lo incluimos para otros motores
        return db.query(Asiento).filter(
            Asiento.asiento_id.in_(ids),
            Asiento.evento_id == evento_id
        ).all() 

    @staticmethod
    def liberar_asientos_de_reserva(db: Session, reserva_id: int):
        """Actualiza el estado de los asientos a DISPONIBLE y limpia reserva_id."""
        db.query(Asiento).filter(
            Asiento.reserva_id == reserva_id
        ).update({
            Asiento.estado: "DISPONIBLE",
            Asiento.reserva_id: None
        }, synchronize_session=False)
        # El commit se hace en el servicio