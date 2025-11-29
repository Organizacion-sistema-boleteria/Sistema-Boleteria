from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.pago_schema import PagoRequest, PagoOut, BoletoSimpleOut
from app.repository.pago_repository import PagoRepository
from app.repository.boleto_repository import BoletoRepository
from app.repository.reserva_repository import ReservaRepository
from app.domain.reserva_model import Reserva
from app.core.pasarela_mock import PasarelaMock # Simulador de pasarela (ver punto 5)
from typing import List
from datetime import datetime, timedelta, timezone 


class PagoService:
    LIMIT_ATTEMPTS = 3

    # --- Lógica de US-011: Procesar Pago ---
    @staticmethod
    def procesar_pago(db: Session, data: PagoRequest, user_id: int) -> PagoOut:
        reserva = ReservaRepository.get_by_id(db, data.reserva_id)

        # 1. Validación de Reserva (Existencia y Pertenencia)
        if not reserva or reserva.usuario_id != user_id:
            raise HTTPException(404, detail={"success": False, "message": "Reserva no encontrada o no válida"})

        # 2. Validación de Estado y Monto
        if reserva.estado != "PENDIENTE":
            raise HTTPException(409, detail={"success": False, "message": f"La reserva ya está {reserva.estado}"})
        
        # En una aplicación real, se recalcula el monto, pero aquí usamos el monto de la reserva:
        if reserva.precio_total != data.monto_solicitado:
            raise HTTPException(400, detail={"success": False, "message": "Monto de pago no coincide con el total de la reserva."})

        # 3. Simulación de Pasarela
        pasarela_result = PasarelaMock.procesar_transaccion(data.monto_solicitado, data.metodo_pago)
        
        pago_estado = pasarela_result["estado"] # APROBADO o RECHAZADO
        ref_externa = pasarela_result["referencia"]
        
        # Iniciar la transacción (ya manejada por FastAPI, solo necesitamos commit/rollback)
        try:
            # 4. Registrar Pago Inicial
            pago = PagoRepository.create(
                db, data.reserva_id, data.monto_solicitado, data.metodo_pago, pago_estado, ref_externa
            )
            
            boletos_out = None
            
            if pago_estado == "APROBADO":
                # 5. Generar Boletos y Confirmar Reserva
                asiento_ids = [a.asiento_id for a in reserva.asientos]
                boletos = BoletoRepository.create_bulk(db, pago.pago_id, asiento_ids)
                
                # 6. Actualizar Reserva a CONFIRMADA
                reserva.estado = "CONFIRMADA"
                # Opcional: Marcar asientos como VENDIDO si la lógica lo requiere aquí
                # for asiento in reserva.asientos: asiento.estado = "VENDIDO"
                db.add(reserva)
                
                boletos_out = [BoletoSimpleOut.model_validate(b) for b in boletos]
                
                db.commit() # Commit para el flujo exitoso
                
                # 7. Mapeo final Pydantic V2 (Solución al error 'update=')
                # Necesitamos un diccionario que contenga el ORM object y la lista anidada
                db.refresh(pago) # Asegura que pago tenga todos los campos actualizados (como intentos=1)
                pago_data = pago.__dict__.copy()
                pago_data["boletos_generados"] = boletos_out
                
                return PagoOut.model_validate(pago_data)

            elif pago_estado == "RECHAZADO":
                # La reserva permanece en PENDIENTE para reintentos (US-012)
                db.commit() # Commit para registrar el pago fallido (intentos=1)
                raise HTTPException(402, detail={"success": False, "message": "Pago rechazado por la pasarela", "error": {"code": 402, "details": pasarela_result["mensaje"]}})
            
        except HTTPException as e:
            db.rollback()
            raise e
        except Exception as e:
            db.rollback()
            raise HTTPException(500, detail={"success": False, "message": "Error interno al procesar el pago", "error": {"code": 500, "details": str(e)}})


    # --- Lógica de US-012: Reintento Automático ---
    @staticmethod
    def reintentar_pagos_automatico(db: Session) -> dict:
        payments_to_retry = PagoRepository.get_payments_to_retry(db, PagoService.LIMIT_ATTEMPTS)
        total_reintentos = 0
        total_aprobados = 0

        for pago in payments_to_retry:
            # Aquí es donde se debe llamar a db.begin_nested() si se usa para commits parciales
            total_reintentos += 1
            pago.intentos += 1
            
            # 1. Simular reintento de Pasarela
            pasarela_result = PasarelaMock.procesar_transaccion(pago.monto, pago.metodo_pago, is_retry=True)
            new_estado = pasarela_result["estado"]

            db.begin_nested() # Transacción anidada para cada pago
            try:
                if new_estado == "APROBADO":
                    # 2. Flujo Exitoso: Actualizar Pago y Generar Boletos
                    pago.estado = new_estado
                    pago.fecha_pago = datetime.utcnow()
                    
                    reserva = ReservaRepository.get_by_id(db, pago.reserva_id)
                    asiento_ids = [a.asiento_id for a in reserva.asientos]

                    BoletoRepository.create_bulk(db, pago.pago_id, asiento_ids)
                    reserva.estado = "CONFIRMADA"
                    
                    total_aprobados += 1
                    db.commit() # Commit de la transacción anidada

                else: # RECHAZADO (Mantiene el estado, solo actualiza el contador de intentos)
                    if pago.intentos >= PagoService.LIMIT_ATTEMPTS:
                         # No requiere cambio de estado (sigue RECHAZADO), solo el commit del intento
                         pass 
                    
                    db.commit() # Commit del intento fallido
                    
            except Exception:
                db.rollback()
                continue

        # Si no hay pagos para reintentar
        if not payments_to_retry:
             return {"total_procesados": 0, "aprobados": 0, "fechaEjecucion": datetime.now(timezone.utc)}
             
        # Guardar cambios finales si hubo algún cambio (solo si se usó begin/commit fuera del bucle, aquí lo omitimos por usar nested commit)
        # db.commit() 
        return {"total_procesados": total_reintentos, "aprobados": total_aprobados, "fechaEjecucion": datetime.now(timezone.utc)}