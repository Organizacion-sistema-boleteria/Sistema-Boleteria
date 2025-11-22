# scripts/init_db.py
import os
import sys

# Asegurar que el root del proyecto esté en el path
sys.path.append(os.path.abspath("."))

from app.database import init_db

# Importar TODOS los modelos del dominio para que SQLAlchemy registre las tablas
from app.domain.usuario_model import Usuario
from app.domain.sede_model import Sede
from app.domain.evento_model import Evento
from app.domain.asiento_model import Asiento
from app.domain.reserva_model import Reserva, Reserva_Asiento
from app.domain.pago_model import Pago
from app.domain.boleto_model import Boleto
from app.domain.reporte_model import Reporte

if __name__ == "__main__":
    init_db()
    print("Base de datos creada con TODAS las tablas del dominio.")
