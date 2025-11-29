from sqlalchemy.orm import Session
from app.domain.boleto_model import Boleto
from typing import List
import uuid # Para generar un codigo_qr único

class BoletoRepository:
    
    @staticmethod
    def create_bulk(db: Session, pago_id: int, asiento_ids: List[int]):
        """Genera boletos para cada asiento asociado al pago."""
        nuevos_boletos = []
        for asiento_id in asiento_ids:
            # Generar Código QR único (simulado con UUID)
            codigo_qr = str(uuid.uuid4()) 
            
            boleto = Boleto(
                pago_id=pago_id,
                asiento_id=asiento_id,
                codigo_qr=codigo_qr,
                estado="VALIDO"
            )
            nuevos_boletos.append(boleto)
        
        db.add_all(nuevos_boletos)
        db.flush() # Se necesita flush para obtener los IDs de los boletos antes de commit
        return nuevos_boletos