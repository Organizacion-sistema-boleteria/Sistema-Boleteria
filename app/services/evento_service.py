from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone # <--- IMPORTANTE: Importamos timezone
from app.schemas.evento_schema import EventoCreate, EventoOut, EventoUpdate
from app.repository.evento_repository import EventoRepository
from app.repository.sede_repository import SedeRepository 
from app.repository.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UsuarioOut

class EventoService:

    @staticmethod
    def validar_reglas_negocio_crear(db: Session, data: EventoCreate):
        # 1. Validar Sede
        sede = SedeRepository.get_by_id(db, data.sede_id)
        if not sede:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"success": False, "message": "La sede seleccionada no existe", "error": {"code": 400, "details": f"Sede ID {data.sede_id} no encontrada"}}
            )
        if sede.estado != "ACTIVA":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"success": False, "message": "La sede seleccionada no está disponible", "error": {"code": 400, "details": "La sede no está en estado ACTIVA"}}
            )
        
        # --- MANEJO DE ZONAS HORARIAS ---
        # Obtenemos la fecha actual en UTC para comparar con la entrada que viene en UTC (Z)
        ahora_utc = datetime.now(timezone.utc)
        
        # Aseguramos que la fecha del evento tenga zona horaria para la comparación
        fecha_evento_comparar = data.fecha_evento
        if fecha_evento_comparar.tzinfo is None:
            fecha_evento_comparar = fecha_evento_comparar.replace(tzinfo=timezone.utc)

        # 2. Validar Fecha Evento Futura
        if fecha_evento_comparar <= ahora_utc:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"success": False, "message": "La fecha del evento debe ser futura", "error": {"code": 400, "details": "La fecha evento es anterior a hoy"}}
            )

        # 3. Validar Cronología de Ventas
        if not (data.fecha_venta_inicio < data.fecha_venta_fin):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"success": False, "message": "La fecha de inicio de venta debe ser anterior a la fecha de fin", "error": {"code": 400, "details": "Rango de fechas de venta inválido"}}
            )
        
        # 4. Validar que la venta termine antes del evento
        if data.fecha_venta_fin > data.fecha_evento:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"success": False, "message": "La venta debe terminar antes del evento", "error": {"code": 400, "details": "Fecha fin venta > Fecha evento"}}
            )

    @staticmethod
    def create(db: Session, data: EventoCreate, current_user: UsuarioOut) -> EventoOut:
        # Asignamos el ID del usuario logueado como organizador
        organizador_id = current_user.usuario_id

        # Ejecutar validaciones de negocio
        EventoService.validar_reglas_negocio_crear(db, data)

        try:
            return EventoRepository.create(db, data, organizador_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"success": False, "message": "Error interno al crear el evento", "error": {"code": 500, "details": str(e)}}
            )

    @staticmethod
    def get_all_publicos(db: Session) -> list:
        # US-006: Solo listar eventos EN_VENTA
        eventos = EventoRepository.list_by_estado(db, estado="EN_VENTA")
        
        # Filtrar eventos pasados usando UTC
        ahora_utc = datetime.now(timezone.utc)
        
        eventos_filtrados = []
        for e in eventos:
            # Normalizar fecha del evento para comparar
            fecha_e = e.fecha_evento
            if fecha_e.tzinfo is None:
                fecha_e = fecha_e.replace(tzinfo=timezone.utc)
            
            if fecha_e >= ahora_utc:
                eventos_filtrados.append(e)
        
        return eventos_filtrados

    @staticmethod
    def get_by_id(db: Session, evento_id: int):
        evento = EventoRepository.get_by_id(db, evento_id)
        if not evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"success": False, "message": "Evento no encontrado", "error": {"code": 404, "details": f"ID {evento_id} no existe"}}
            )
        return evento

    @staticmethod
    def update(db: Session, evento_id: int, data: EventoUpdate, current_user: UsuarioOut):
        evento = EventoService.get_by_id(db, evento_id)

        # Regla: Solo el dueño del evento o un Admin pueden editarlo
        if current_user.rol != "ADMINISTRADOR" and evento.organizador_id != current_user.usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"success": False, "message": "Permiso denegado", "error": {"code": 403, "details": "No puedes editar un evento que no es tuyo."}}
            )
        
        return EventoRepository.update(db, evento, data)

    @staticmethod
    def delete(db: Session, evento_id: int):
        evento = EventoService.get_by_id(db, evento_id)
        EventoRepository.delete(db, evento)