from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from app.repository.reserva_repository import ReservaRepository
from app.repository.asiento_repository import AsientoRepository
from app.domain.reserva_model import Reserva
from app.schemas.reserva_schema import ReservaCreateRequest, ReservaData, ExpiracionData
from app.schemas.usuario_schema import UsuarioOut
from typing import List

class ReservaService:
    LIMIT_ASIENTOS = 8
    TIEMPO_EXPIRACION_MIN = 15

    @staticmethod
    def _map_to_schema(reserva: Reserva, asientos_ids: List[int]) -> ReservaData:
        """Helper para mapear modelo a ReservaData."""
        return ReservaData(
            reservaId=reserva.reserva_id,
            usuarioId=reserva.usuario_id,
            eventoId=reserva.evento_id,
            asientosReservados=asientos_ids,
            precioTotal=reserva.precio_total,
            fechaReserva=reserva.fecha_reserva,
            fechaExpiracion=reserva.fecha_expiracion,
            estado=reserva.estado
        )

    @staticmethod
    def crear_reserva(db: Session, request: ReservaCreateRequest, usuario_id: int):
        # 1. Validaciones de límites
        if not request.asientos: raise HTTPException(status_code=400, detail="Debe seleccionar al menos un asiento.")
        if len(request.asientos) < 1 or len(request.asientos) > ReservaService.LIMIT_ASIENTOS:
            raise HTTPException(status_code=400, detail=f"El número de asientos debe estar entre 1 y {ReservaService.LIMIT_ASIENTOS}.")

        # 2. Obtener y Bloquear Asientos (Transacción Atómica)
        asientos_db = ReservaRepository.get_asientos_by_ids_lock(db, request.asientos, request.evento_id)

        # 3. Validar existencia y unicidad
        if len(asientos_db) != len(request.asientos):
            raise HTTPException(status_code=404, detail="Uno o más asientos no fueron encontrados en este evento.")

        # 4. Validar disponibilidad
        asientos_ocupados = [f"Asiento {a.seccion}-{a.fila}-{a.numero}" for a in asientos_db if a.estado != "DISPONIBLE"]
        if asientos_ocupados:
            return {
                "success": False,
                "message": "Uno o más asientos ya están reservados",
                "error_details": asientos_ocupados
            }

        # 5. Cálculo y Fechas
        precio_total = sum(a.precio for a in asientos_db)
        fecha_now = datetime.utcnow()
        fecha_exp = fecha_now + timedelta(minutes=ReservaService.TIEMPO_EXPIRACION_MIN)

        nueva_reserva = Reserva(
            usuario_id=usuario_id,
            evento_id=request.evento_id,
            precio_total=precio_total,
            fecha_reserva=fecha_now,
            fecha_expiracion=fecha_exp,
            estado="PENDIENTE"
        )
        
        # 6. Guardar Reserva y obtener ID (Flush)
        db.add(nueva_reserva)
        db.flush() # Obtiene el reserva_id

        # 7. Actualizar Asientos y Asignar Reserva_ID
        asientos_ids = []
        for asiento in asientos_db:
            asiento.estado = "RESERVADO"
            asiento.reserva_id = nueva_reserva.reserva_id
            asientos_ids.append(asiento.asiento_id)
        
        db.commit()

        return {
            "success": True,
            "message": "Reserva creada exitosamente",
            "data": ReservaService._map_to_schema(nueva_reserva, asientos_ids)
        }

    @staticmethod
    def cancelar_reservas_expiradas(db: Session):
        """[US-010] Proceso automático para liberar asientos."""
        reservas = ReservaRepository.obtener_pendientes_expiradas(db)
        
        if not reservas:
            return {"success": True, "message": "No se encontraron reservas expiradas", 
                    "data": {"reservasCanceladas": 0, "asientosLiberados": 0, "fechaEjecucion": datetime.utcnow()}}

        count_res = 0
        count_asi = 0
        reservas_ids = [r.reserva_id for r in reservas]

        # 1. Liberar asientos masivamente
        for reserva_id in reservas_ids:
            # (No podemos usar .reserva_id = None en la query si no cargamos la relación)
            # Usaremos una query de update directa si fuera posible, pero iteramos por seguridad
            asientos_liberados = AsientoRepository.get_by_evento(db, reservas[0].evento_id)
            for a in asientos_liberados:
                if a.reserva_id in reservas_ids:
                    a.estado = "DISPONIBLE"
                    a.reserva_id = None
                    count_asi += 1

        # 2. Actualizar estado de las reservas
        db.query(Reserva).filter(Reserva.reserva_id.in_(reservas_ids)).update(
            {Reserva.estado: "EXPIRADA"}, synchronize_session=False
        )
        count_res = len(reservas_ids)
        
        db.commit()
        return {
            "success": True, 
            "message": "Reservas expiradas canceladas correctamente", 
            "data": {"reservasCanceladas": count_res, "asientosLiberados": count_asi, "fechaEjecucion": datetime.utcnow()}
        }
    
    @staticmethod
    def obtener_por_usuario(db: Session, usuario_id: int):
        # Lógica para listar reservas
        pass # Implementación pendiente, no requerida por el core

    @staticmethod
    def obtener_detalle(db: Session, reserva_id: int, usuario_id: int, es_admin: bool):
        # Lógica para ver detalle
        pass # Implementación pendiente, no requerida por el core

    @staticmethod
    def cancelar_manual(db: Session, reserva_id: int, usuario_id: int):
        # Lógica para cancelar manualmente
        pass # Implementación pendiente, no requerida por el core