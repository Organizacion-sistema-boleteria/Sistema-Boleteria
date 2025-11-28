from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.asiento_schema import *
from app.repository.asiento_repository import AsientoRepository
from app.repository.evento_repository import EventoRepository
from app.repository.sede_repository import SedeRepository
from app.domain.asiento_model import Asiento
from app.schemas.usuario_schema import UsuarioOut

class AsientoService:
    @staticmethod
    def crear_asientos_masivos(db: Session, evento_id: int, data: AsientosCreateRequest, current_user: UsuarioOut):
        evento = EventoRepository.get_by_id(db, evento_id)
        if not evento: raise HTTPException(404, detail={"success": False, "message": "Evento no encontrado"})
        if current_user.rol != "ADMINISTRADOR" and evento.organizador_id != current_user.usuario_id: raise HTTPException(403, detail={"success": False, "message": "Permisos insuficientes"})
        if AsientoRepository.count_by_evento(db, evento_id) > 0: raise HTTPException(409, detail={"success": False, "message": "El evento ya tiene asientos"})

        total = sum(sum(f.asientos for f in s.filas) for s in data.secciones)
        sede = SedeRepository.get_by_id(db, evento.sede_id)
        if total > sede.capacidad_total: raise HTTPException(400, detail={"success": False, "message": "Capacidad excedida"})

        nuevos = []
        dist = []
        for s in data.secciones:
            cant = 0
            for f in s.filas:
                cant += f.asientos
                for i in range(1, f.asientos + 1):
                    nuevos.append(Asiento(evento_id=evento.evento_id, seccion=s.nombre, fila=f.fila, numero=str(i), precio=s.precio, tipo=s.tipo))
            dist.append(DistribucionItem(seccion=s.nombre, cantidad=cant, precio=s.precio))

        AsientoRepository.create_bulk(db, nuevos)
        return ResumenCreacionData(eventoId=evento.evento_id, titulo=evento.titulo, totalAsientosCreados=total, capacidadSede=sede.capacidad_total, distribucion=dist)

    @staticmethod
    def consultar_disponibilidad(db: Session, evento_id: int):
        if not EventoRepository.get_by_id(db, evento_id): raise HTTPException(404, detail={"success": False, "message": "Evento no encontrado"})
        asientos = AsientoRepository.get_by_evento(db, evento_id)
        return DisponibilidadData(
            eventoId=evento_id, titulo="Evento", fechaEvento="", # Se puede mejorar consultando el evento de nuevo
            totalAsientos=len(asientos), disponibles=sum(1 for a in asientos if a.estado == "DISPONIBLE"),
            reservados=sum(1 for a in asientos if a.estado == "RESERVADO"), vendidos=sum(1 for a in asientos if a.estado == "VENDIDO"), asientos=asientos
        )

    @staticmethod
    def update(db: Session, id: int, data: AsientoUpdate):
        a = AsientoRepository.get_by_id(db, id)
        if not a: raise HTTPException(404, detail="Asiento no encontrado")
        return AsientoRepository.update(db, a, data)

    @staticmethod
    def delete(db: Session, id: int):
        a = AsientoRepository.get_by_id(db, id)
        if not a: raise HTTPException(404, detail="Asiento no encontrado")
        AsientoRepository.delete(db, a)