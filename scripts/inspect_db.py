# scripts/inspect_db.py

from sqlalchemy import create_engine, inspect
from app.database import DATABASE_URL

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

print("\n=== Tablas encontradas ===")
tables = inspector.get_table_names()
for table in tables:
    print(f"- {table}")

print("\n=== Estructura de tablas ===")
for table in tables:
    print(f"\nTabla: {table}")
    columns = inspector.get_columns(table)
    for col in columns:
        print(f"  {col['name']} ({col['type']})")
