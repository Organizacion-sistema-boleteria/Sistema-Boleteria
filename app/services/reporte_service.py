# app/services/reporte_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository.reporte_repository import ReporteRepository
from app.schemas.reporte_schema import ReporteCreate, ReporteUpdate
from app.domain.reporte_model import Reporte


class ReporteService:

    @staticmethod
    def create(db: Session, data: ReporteCreate) -> Reporte:
        return ReporteRepository.create(db, data)

    @staticmethod
    def get(db: Session, reporte_id: int):
        reporte = ReporteRepository.get_by_id(db, reporte_id)
        if not reporte:
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        return reporte

    @staticmethod
    def list(db: Session):
        return ReporteRepository.list(db)

    @staticmethod
    def update(db: Session, reporte_id: int, data: ReporteUpdate):
        reporte = ReporteService.get(db, reporte_id)
        return ReporteRepository.update(db, reporte, data)

    @staticmethod
    def delete(db: Session, reporte_id: int):
        reporte = ReporteService.get(db, reporte_id)
        ReporteRepository.delete(db, reporte)
        return {"message": "Reporte eliminado correctamente"}

    # ---------------------------
    # REPORTES ESPECIALES
    # ---------------------------

    @staticmethod
    def ventas_por_evento(db: Session, evento_id: int):
        """
        Retorna:
        - boletos_vendidos
        - ingresos (suma de pagos aprobados)
        - reservas_confirmadas
        """

        # Boletos vendidos por evento
        q1 = """
            SELECT COUNT(b.boleto_id)
            FROM boletos b
            JOIN asientos a ON b.asiento_id = a.asiento_id
            WHERE a.evento_id = :evento_id
        """
        boletos = db.execute(q1, {"evento_id": evento_id}).fetchone()[0]

        # Ingresos del evento (solo pagos aprobados)
        q2 = """
            SELECT COALESCE(SUM(p.monto), 0)
            FROM pagos p
            JOIN reservas r ON p.reserva_id = r.reserva_id
            WHERE r.evento_id = :evento_id
              AND p.estado = 'APROBADO'
        """
        ingresos = float(db.execute(q2, {"evento_id": evento_id}).fetchone()[0])

        # Reservas confirmadas
        q3 = """
            SELECT COUNT(*)
            FROM reservas
            WHERE evento_id = :evento_id
              AND estado = 'CONFIRMADA'
        """
        reservas = db.execute(q3, {"evento_id": evento_id}).fetchone()[0]

        return {
            "evento_id": evento_id,
            "boletos_vendidos": boletos,
            "ingresos": ingresos,
            "reservas_confirmadas": reservas
        }

    @staticmethod
    def general_summary(db: Session):
        """
        Devuelve:
        - total_eventos
        - total_usuarios
        - total_boletos
        - ingresos_totales
        """

        q = """
            SELECT
                (SELECT COUNT(*) FROM eventos) AS total_eventos,
                (SELECT COUNT(*) FROM usuarios) AS total_usuarios,
                (SELECT COUNT(*) FROM boletos) AS total_boletos,
                (SELECT COALESCE(SUM(monto), 0) FROM pagos WHERE estado='APROBADO') AS ingresos_totales
        """

        res = db.execute(q).fetchone()
        if not res:
            raise HTTPException(status_code=500, detail="Error generando reporte")

        return {
            "total_eventos": int(res[0]),
            "total_usuarios": int(res[1]),
            "total_boletos": int(res[2]),
            "ingresos_totales": float(res[3])
        }
