from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from app.schemas.evento_schema import EventoCreate, EventoOut
from app.repository.evento_repository import EventoRepository
# Importamos repositorios para validaciones cruzadas
from app.repository.sede_repository import SedeRepository 
from app.repository.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UsuarioOut

class EventoService:

    @staticmethod
    def validar_reglas_negocio_crear(db: Session, data: EventoCreate):
        # 1. Validar Sede (US-005): Debe existir y estar ACTIVA
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
        
        # 2. Validar Fecha Evento Futura (US-005)
        # datetime.utcnow() es mejor para servidores, pero usa lo que prefieras
        if data.fecha_evento <= datetime.now():
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"success": False, "message": "La fecha del evento debe ser futura", "error": {"code": 400, "details": "La fecha evento es anterior a hoy"}}
            )

        # 3. Validar Cronología de Ventas (US-005)
        if not (data.fecha_venta_inicio < data.fecha_venta_fin):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"success": False, "message": "La fecha de inicio de venta debe ser anterior a la fecha de fin", "error": {"code": 400, "details": "Rango de fechas de venta inválido"}}
            )
        
        # 4. Validar que la venta termine antes del evento (Lógica común)
        if data.fecha_venta_fin > data.fecha_evento:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"success": False, "message": "La venta debe terminar antes del evento", "error": {"code": 400, "details": "Fecha fin venta > Fecha evento"}}
            )

    @staticmethod
    def create(db: Session, data: EventoCreate, current_user: UsuarioOut) -> EventoOut:
        # El organizador es el usuario del token (US-005)
        organizador_id = current_user.usuario_id

        # Ejecutar validaciones de negocio
        EventoService.validar_reglas_negocio_crear(db, data)

        try:
            # Crear evento pasando el organizador_id
            evento_creado = EventoRepository.create(db, data, organizador_id)
            return evento_creado
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"success": False, "message": "Error interno al crear el evento", "error": {"code": 500, "details": str(e)}}
            )

    @staticmethod
    def get_all_publicos(db: Session) -> list:
        # US-006: Solo listar eventos EN_VENTA
        eventos = EventoRepository.list_by_estado(db, estado="EN_VENTA")
        
        # Filtrar eventos pasados (US-006 Nota Técnica: fechaEvento >= hoy)
        eventos_filtrados = [e for e in eventos if e.fecha_evento >= datetime.now()]
        
        return eventos_filtrados