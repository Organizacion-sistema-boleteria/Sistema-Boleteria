# test_flow.py
import os, sys
sys.path.append(os.path.abspath("."))

from sqlalchemy.orm import Session
from app.database import SessionLocal

# Services
from app.services.usuario_service import UsuarioService
from app.services.sede_service import SedeService
from app.services.evento_service import EventoService
from app.services.reserva_service import ReservaService
from app.services.pago_service import PagoService
from app.services.asiento_service import AsientoService
from app.services.boleto_service import BoletoService

# Schemas
from app.schemas.usuario_schema import UsuarioCreate
from app.schemas.sede_schema import SedeCreate
from app.schemas.evento_schema import EventoCreate
from app.schemas.asiento_schema import AsientoCreate
from app.schemas.reserva_schema import ReservaCreate
from app.schemas.pago_schema import PagoCreate

from datetime import datetime, timedelta


def db():
    return SessionLocal()


print("\n========== INICIANDO TEST ==========\n")

session = db()

# 1. Crear usuario
print("1) Creando usuario...")
u = UsuarioService.create(session, UsuarioCreate(
    nombre="Usuario Test",
    email="test@test.com",
    telefono="12345",
    password="hash",
    rol="cliente",
    estado="activo"
))
print("Usuario creado:", u.usuario_id)

# 2. Crear sede
print("\n2) Creando sede...")
s = SedeService.create(session, SedeCreate(
    nombre="Sede Principal",
    direccion="Calle 1",
    ciudad="Ciudad X",
    capacidad_total=1000,
    descripcion="Desc",
    estado="activo"
))
print("Sede creada:", s.sede_id)

# 3. Crear evento
print("\n3) Creando evento...")
e = EventoService.create(session, EventoCreate(
    sede_id=s.sede_id,
    organizador_id=u.usuario_id,
    titulo="Concierto Test",
    descripcion="Evento",
    fecha_evento=datetime.utcnow() + timedelta(days=5),
    fecha_venta_inicio=datetime.utcnow(),
    fecha_venta_fin=datetime.utcnow() + timedelta(days=3),
    precio_base=50.0,
    categoria="Musica",
    estado="activo"
))
print("Evento creado:", e.evento_id)

# 4. Crear asientos
print("\n4) Creando asientos...")
a1 = AsientoService.create(session, AsientoCreate(
    evento_id=e.evento_id,
    seccion="A",
    fila="1",
    numero="10",
    precio=100.0,
    tipo="VIP"
))

a2 = AsientoService.create(session, AsientoCreate(
    evento_id=e.evento_id,
    seccion="A",
    fila="1",
    numero="11",
    precio=100.0,
    tipo="VIP"
))
print("Asientos creados:", a1.asiento_id, a2.asiento_id)

# 5. Crear reserva
print("\n5) Creando reserva...")
r = ReservaService.create(session, ReservaCreate(
    usuario_id=u.usuario_id,
    evento_id=e.evento_id,
    fecha_expiracion=datetime.utcnow() + timedelta(minutes=10),
    estado="ACTIVA",
    precio_total=0,
    asientos_ids=[a1.asiento_id, a2.asiento_id]
))
print("Reserva creada:", r.reserva_id)
print("Precio total:", r.precio_total)

# 6. Pago
print("\n6) Realizando pago...")
pago = PagoService.create(session, PagoCreate(
    reserva_id=r.reserva_id,
    monto=r.precio_total,
    metodo_pago="tarjeta",
    estado="APROBADO"
))
print("Pago realizado:", pago["pago"].pago_id)
print("Boletos generados:", len(pago["boletos"]))

# 7. Validar boletos
print("\n7) Validando boletos...")
for b in pago["boletos"]:
    print(f"Boleto {b.boleto_id} → asiento={b.asiento_id}  qr={b.codigo_qr}")

# 8. Estados de asientos
print("\n8) Revisando estados...")
a1_refrescado = AsientoService.get(session, a1.asiento_id)
a2_refrescado = AsientoService.get(session, a2.asiento_id)
print("Asiento 1 estado:", a1_refrescado.estado)
print("Asiento 2 estado:", a2_refrescado.estado)

print("\n========== TEST COMPLETADO ==========\n")
