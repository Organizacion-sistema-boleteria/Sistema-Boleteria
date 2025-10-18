# Sistema de Boletería para Eventos

## Descripción

Sistema de venta de boletos digitales que permite a los usuarios comprar entradas para eventos y a los organizadores gestionar sus actividades. Resuelve problemas comunes como páginas confusas, errores al seleccionar asientos, fallas en pagos y falta de control en tiempo real del inventario.

## Objetivo

Desarrollar una solución que mejore la experiencia de compra para los usuarios y facilite la administración de eventos para los organizadores mediante un sistema robusto y transparente.

---

## Contexto del Problema

En Colombia, plataformas como TuBoleta y eTicket presentan problemas técnicos frecuentes con boletos electrónicos. Qubit tuvo que desarrollar algoritmos específicos para combatir la duplicación de códigos QR, y la Superintendencia de Industria y Comercio ha investigado a operadores por no informar alternativas ante cancelación de eventos.

---

## Arquitectura del Sistema

El sistema está organizado en cuatro capas:

### Capa de Dominio
Define las entidades del negocio con sus atributos y relaciones. Contiene la lógica fundamental sin depender de tecnologías específicas.

### Capa de Repositorio
Maneja la persistencia de datos en base de datos relacional, definiendo tablas, tipos de datos y relaciones.

### Capa de Servicio
Implementa la lógica de negocio: validaciones, reglas de reserva, liberación automática de asientos, generación de boletos.

### Capa de API
Expone endpoints REST que permiten la comunicación con el sistema mediante JSON.

---

## Entidades del Sistema

### Usuario
Personas que interactúan con el sistema.

**Roles disponibles:**
- CLIENTE
- ORGANIZADOR
- ADMINISTRADOR

**Atributos principales:**
- usuarioId
- nombre
- email
- telefono
- passwordHash
- rol
- fechaRegistro
- estado

---

### Sede
Lugares físicos donde se realizan los eventos.

**Atributos principales:**
- sedeId
- nombre
- direccion
- ciudad
- capacidadTotal
- descripcion
- estado

---

### Evento
Actividades programadas para venta de boletos.

**Atributos principales:**
- eventoId
- titulo
- descripcion
- fechaEvento
- fechaVentaInicio
- fechaVentaFin
- precioBase
- categoria
- estado

---

### Asiento
Unidades de inventario dentro de cada evento.

**Atributos principales:**
- asientoId
- eventoId
- seccion
- fila
- numero
- precio
- tipo
- estado

---

### Reserva
Bloqueo temporal de asientos mientras el usuario completa la compra.

**Tiempo de expiración:** 15 minutos

**Atributos principales:**
- reservaId
- usuarioId
- eventoId
- asientosReservados
- precioTotal
- fechaReserva
- fechaExpiracion
- estado

---

### Pago
Registro de transacciones financieras.

**Atributos principales:**
- pagoId
- reservaId
- monto
- metodoPago
- estado
- fechaPago
- referenciaExterna

---

### Boleto
Comprobante digital con código QR único para acceso al evento.

**Atributos principales:**
- boletoId
- pagoId
- asientoId
- codigoQR
- fechaEmision
- estado
- fechaUso

---

### Reporte
Consolidados de ventas, ocupación e ingresos para organizadores.

**Atributos principales:**
- reporteId
- tipoReporte
- eventoId
- fechaGeneracion
- parametros
- datos

---

## Módulos de API

### API de Usuarios
- `POST /api/usuarios` - Registrar usuario
- `POST /api/usuarios/login` - Autenticación
- `GET /api/usuarios/{id}` - Consultar perfil
- `PUT /api/usuarios/{id}` - Actualizar perfil
- `DELETE /api/usuarios/{id}` - Eliminar usuario

### API de Sedes
- `POST /api/sedes` - Crear sede
- `GET /api/sedes` - Listar sedes
- `GET /api/sedes/{id}` - Consultar detalle
- `PUT /api/sedes/{id}` - Actualizar sede
- `DELETE /api/sedes/{id}` - Deshabilitar sede

### API de Eventos
- `POST /api/eventos` - Crear evento
- `GET /api/eventos` - Listar eventos disponibles
- `GET /api/eventos/{id}` - Consultar detalle
- `PUT /api/eventos/{id}` - Modificar evento
- `DELETE /api/eventos/{id}` - Cancelar evento

### API de Asientos
- `GET /api/eventos/{id}/asientos` - Ver disponibilidad
- `PUT /api/asientos/{id}/liberar` - Liberar asiento

### API de Reservas
- `POST /api/reservas` - Crear reserva
- `GET /api/reservas/{id}` - Consultar reserva
- `PUT /api/reservas/{id}/confirmar` - Confirmar reserva
- `DELETE /api/reservas/{id}` - Cancelar reserva

### API de Pagos
- `POST /api/pagos` - Procesar pago
- `GET /api/pagos/{id}` - Consultar estado
- `POST /api/pagos/mock` - Simular pago (pruebas)

### API de Boletos
- `POST /api/boletos` - Generar boleto
- `GET /api/boletos/{id}` - Consultar boleto
- `GET /api/boletos/usuario/{id}` - Boletos de usuario
- `GET /api/boletos/validar/{qr}` - Validar boleto en acceso

### API de Reportes
- `GET /api/reportes/eventos/{id}` - Reporte de ventas por evento
- `GET /api/reportes/usuarios/{id}` - Historial de compras
- `GET /api/reportes/general` - Reporte consolidado

---

## Formato de Respuesta JSON

Todas las respuestas siguen esta estructura estandarizada:

```json
{
  "success": true,
  "message": "Descripción del resultado",
  "data": {},
  "error": {}
}
```

### Ejemplo de respuesta exitosa:

```json
{
  "success": true,
  "message": "Usuario creado exitosamente",
  "data": {
    "usuarioId": 1,
    "nombre": "Juan Pérez",
    "email": "juan@email.com",
    "rol": "CLIENTE",
    "fechaRegistro": "2025-09-08T15:30:00Z"
  }
}
```

### Ejemplo de respuesta con error:

```json
{
  "success": false,
  "message": "El asiento seleccionado ya está reservado",
  "error": {
    "code": 409,
    "details": "Asiento ID 15 en el evento 10 no está disponible"
  }
}
```

---

## Reglas de Negocio

### Asientos
- Solo pueden tener un estado a la vez: DISPONIBLE, RESERVADO o VENDIDO
- Los asientos reservados se liberan automáticamente si expira el tiempo de reserva
- Una vez vendidos, no pueden volver a estar disponibles

### Reservas
- Tiempo máximo de validez: 15 minutos
- Solo se pueden crear si la venta del evento está activa
- Mínimo 1 asiento, máximo 8 asientos por reserva

### Pagos
- Cada reserva se confirma con un único pago
- Pagos rechazados liberan los asientos automáticamente
- Pagos aprobados generan boletos digitales

### Boletos
- Código QR único por boleto
- Solo pueden validarse una vez
- Al usarse cambian a estado USADO

### Capacidad
- La suma de asientos de un evento no puede superar la capacidad de la sede
- No se permite sobreventa

### Roles de Usuario
- Solo ORGANIZADORES pueden crear eventos
- CLIENTES solo acceden a sus propias reservas y boletos
- ADMINISTRADORES tienen control global y generan reportes

---

## Tecnologías

| Componente | Tecnología |
|-----------|-----------|
| Arquitectura | REST |
| Formato de datos | JSON |
| Base de datos | Relacional |
| Formato de fechas | ISO 8601 (YYYY-MM-DDTHH:mm:ssZ) |
| Autenticación | JWT |

---

## Códigos HTTP

### Respuestas de Éxito
- `200 OK` - Operación exitosa
- `201 Created` - Recurso creado
- `204 No Content` - Acción realizada sin datos

### Errores del Cliente
- `400 Bad Request` - Datos inválidos o incompletos
- `401 Unauthorized` - Falta autenticación
- `403 Forbidden` - Permisos insuficientes
- `404 Not Found` - Recurso no encontrado
- `409 Conflict` - Conflicto de operación

### Errores del Servidor
- `500 Internal Server Error` - Fallo inesperado
- `503 Service Unavailable` - Servicio no disponible

---

## Documentación

Para más detalles sobre la arquitectura, capas y diagramas, consultar el [Entregable #1](./docs/entregable1.pdf)

---

## Autor

**Juan Felipe Huérfano Rúa**  
Tecnología en Desarrollo de Sistemas Informáticos  
Unidades Tecnológicas de Santander  
Bucaramanga, Colombia

**Fecha:** Septiembre 2025
