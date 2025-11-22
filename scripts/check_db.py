import os
import sys

# Añadir root del proyecto al PATH (igual que init_db.py)
sys.path.append(os.path.abspath("."))

from app.database import engine
from sqlalchemy import inspect

insp = inspect(engine)

print("Tablas encontradas en la base de datos:")
print(insp.get_table_names())
