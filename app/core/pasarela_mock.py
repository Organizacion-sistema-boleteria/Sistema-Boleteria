import random

class PasarelaMock:
    
    @staticmethod
    def procesar_transaccion(monto: float, metodo: str, is_retry: bool = False) -> dict:
        """Simula la comunicación con una pasarela de pagos externa."""
        
        # Lógica para forzar un fallo o un éxito para las pruebas:
        if monto == 999999.00:
            return {"estado": "RECHAZADO", "referencia": "MOCK-FAIL-HIGH", "mensaje": "Fondo insuficiente forzado."}
        
        if metodo == "MOCK_RECHAZO_TEMPORAL":
            # Usado en US-012 para simular rechazos que eventualmente pasan
            if is_retry:
                 return {"estado": "APROBADO", "referencia": "MOCK-PASS-RETRY", "mensaje": "Pago aprobado al reintentar."}
            else:
                 return {"estado": "RECHAZADO", "referencia": "MOCK-FAIL-RETRY-1", "mensaje": "Rechazo inicial forzado."}
                 
        # Lógica aleatoria o éxito por defecto:
        if random.random() < 0.95 or is_retry: 
            return {"estado": "APROBADO", "referencia": f"TXN-{random.randint(1000, 9999)}", "mensaje": "Transacción exitosa."}
        else:
            return {"estado": "RECHAZADO", "referencia": f"TXN-FAIL-{random.randint(1000, 9999)}", "mensaje": "Error genérico de la pasarela."}