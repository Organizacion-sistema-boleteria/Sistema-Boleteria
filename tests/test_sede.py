from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app


client = TestClient(app)

# HU-001: Crear sede
def test_crear_sede():
    data = {
        "nombre": "Sede Central",
        "direccion": "Calle 123",
        "ciudad": "Bogotá"
    }
    response = client.post("/api/v1/sedes/", json=data)
    assert response.status_code == 201
    body = response.json()
    assert body["nombre"] == "Sede Central"

# HU-002: Listar sedes
def test_listar_sedes():
    response = client.get("/api/v1/sedes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# HU-003: Obtener sede por ID
def test_obtener_sede():
    response = client.get("/api/v1/sedes/1")
    assert response.status_code in [200, 404]

# HU-004: Actualizar sede
def test_actualizar_sede():
    data = {"nombre": "Sede Actualizada"}
    response = client.put("/api/v1/sedes/1", json=data)
    assert response.status_code in [200, 404]

# HU-005: Eliminar sede
def test_eliminar_sede():
    response = client.delete("/api/v1/sedes/1")
    assert response.status_code in [204, 404]
