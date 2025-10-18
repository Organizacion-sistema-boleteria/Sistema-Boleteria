# Alcance del Proyecto - Sistema de Boletería

## Objetivo General

Desarrollar un sistema de boletería digital basado en arquitectura REST que permita la venta de boletos para eventos, mejorando la experiencia del usuario en el proceso de compra y facilitando la gestión administrativa para los organizadores.

---

## Alcance Incluido

### Funcionalidades Principales

**Gestión de Usuarios**
- Registro de nuevos usuarios en el sistema
- Autenticación mediante credenciales (email y contraseña)
- Consulta y actualización de perfiles de usuario
- Administración de roles: CLIENTE, ORGANIZADOR, ADMINISTRADOR

**Gestión de Sedes**
- Registro de sedes con capacidad y ubicación
- Consulta de sedes disponibles
- Actualización de información de sedes
- Control de estado de sedes (ACTIVA, INACTIVA, MANTENIMIENTO)

**Gestión de Eventos**
- Creación de eventos por parte de organizadores
- Publicación de eventos disponibles para venta
- Consulta de detalle de eventos
- Modificación y cancelación de eventos
- Control de fechas de venta (inicio y fin)

**Gestión de Asientos**
- Consulta de disponibilidad de asientos por evento
- Control de estados: DISPONIBLE, RESERVADO, VENDIDO
- Liberación automática de asientos cuando expiran reservas
- Bloqueo de asientos durante proceso de reserva

**Gestión de Reservas**
- Creación de reservas con bloqueo temporal de asientos
- Tiempo de expiración de 15 minutos
- Confirmación de reservas para proceder al pago
- Cancelación de reservas
- Liberación automática de asientos al expirar

**Gestión de Pagos**
- Procesamiento de transacciones de pago
- Validación de métodos de pago
- Registro de estado de pagos (PENDIENTE, APROBADO, RECHAZADO)
- Generación automática de boletos tras pago aprobado

**Gestión de Boletos**
- Emisión de boletos digitales con código QR único
- Consulta de boletos por usuario
- Validación de boletos en puntos de acceso
- Control de uso único de boletos

**Generación de Reportes**
- Reportes de ventas por evento
- Análisis de ocupación de sedes
- Historial de compras por usuario
- Reportes consolidados de ingresos

---

## Entregables por Sprint

### Sprint 1: Módulo de Usuarios (Semanas 1-2)

**Historias de Usuario:**
- HU-001: Registrar Usuario en el Sistema
- HU-002: Autenticación de Usuario
- HU-003: Consultar Perfil de Usuario
- HU-004: Actualizar Perfil de Usuario

**Entregables técnicos:**
- Endpoints de usuarios implementados y funcionales
- Tabla usuario creada en base de datos
- Sistema de encriptación de contraseñas implementado
- Generación de tokens JWT funcional
- Pruebas unitarias de autenticación

---

### Sprint 2: Módulo de Eventos y Sedes (Semanas 3-4)

**Historias de Usuario:**
- HU-005: Crear Sede
- HU-006: Consultar Sedes Disponibles
- HU-007: Crear Evento
- HU-008: Consultar Eventos Disponibles
- HU-009: Consultar Detalle de Evento

**Entregables técnicos:**
- Endpoints de sedes y eventos implementados
- Tablas sede y evento creadas en base de datos
- Relación entre sedes y eventos funcional
- Validación de roles para creación de eventos
- Pruebas de consulta y filtrado de eventos

---

### Sprint 3: Módulo de Asientos y Reservas (Semanas 5-7)

**Historias de Usuario:**
- HU-010: Ver Disponibilidad de Asientos
- HU-011: Crear Reserva
- HU-012: Confirmar Reserva
- HU-013: Cancelar Reserva

**Entregables técnicos:**
- Endpoints de asientos y reservas implementados
- Tablas asiento, reserva y reserva_asiento creadas
- Sistema de liberación automática de asientos implementado
- Control de tiempo de expiración de reservas
- Validación de capacidad y disponibilidad

---

### Sprint 4: Módulo de Pagos y Boletos (Semanas 8-9)

**Historias de Usuario:**
- HU-014: Procesar Pago
- HU-015: Consultar Estado de Pago
- HU-016: Generar Boleto Digital
- HU-017: Validar Boleto con QR

**Entregables técnicos:**
- Endpoints de pagos y boletos implementados
- Tablas pago y boleto creadas
- Generación de códigos QR únicos
- Sistema de validación de boletos
- Simulador de pagos para pruebas

---

### Sprint 5: Módulo de Reportes y Ajustes Finales (Semanas 10-11)

**Historias de Usuario:**
- HU-018: Generar Reporte de Ventas por Evento
- HU-019: Consultar Historial de Compras
- HU-020: Reporte Consolidado General

**Entregables técnicos:**
- Endpoints de reportes implementados
- Tabla reporte creada
- Consultas optimizadas para reportes
- Documentación completa en Swagger
- Pruebas de integración finales

---

## Cronograma

| Sprint | Duración | Inicio | Fin | Entregables |
|--------|----------|--------|-----|-------------|
| Sprint 1 | 2 semanas | Semana 1 | Semana 2 | Módulo Usuarios |
| Sprint 2 | 2 semanas | Semana 3 | Semana 4 | Módulo Eventos y Sedes |
| Sprint 3 | 3 semanas | Semana 5 | Semana 7 | Módulo Asientos y Reservas |
| Sprint 4 | 2 semanas | Semana 8 | Semana 9 | Módulo Pagos y Boletos |
| Sprint 5 | 2 semanas | Semana 10 | Semana 11 | Módulo Reportes |

**Duración total del proyecto:** 11 semanas

---

## Criterios de Éxito

El proyecto se considerará exitoso cuando:

1. **Funcionalidad Completa**
   - Todos los endpoints definidos funcionan correctamente
   - Las validaciones de negocio están implementadas
   - El sistema maneja correctamente los estados de asientos y reservas

2. **Calidad del Código**
   - Código organizado en capas (Dominio, Repositorio, Servicio, API)
   - Nomenclatura consistente y clara
   - Separación de responsabilidades correcta

3. **Pruebas**
   - Todas las pruebas unitarias pasan exitosamente
   - Casos de error están cubiertos
   - Validaciones funcionan según lo esperado

4. **Documentación**
   - Cada endpoint está documentado con ejemplos
   - Estructuras JSON están definidas
   - Códigos de error están especificados

5. **Seguridad**
   - Contraseñas encriptadas correctamente
   - Tokens JWT implementados
   - Control de acceso por roles funcional

6. **Experiencia de Usuario**
   - Respuestas JSON estandarizadas
   - Mensajes de error claros
   - Tiempos de respuesta aceptables

---

## Restricciones y Limitaciones

### Restricciones Técnicas
- El sistema usa arquitectura REST
- Base de datos relacional
- Formato de intercambio de datos: JSON únicamente
- Fechas en formato ISO 8601

### Limitaciones de Negocio
- Tiempo máximo de reserva: 15 minutos
- Máximo 8 asientos por reserva
- No se permite sobreventa de asientos
- Un boleto solo puede validarse una vez

### Dependencias Externas
- Sistema de encriptación para contraseñas
- Generador de tokens JWT
- Generador de códigos QR

---

## Fuera de Alcance (Versión 1.0)

Lo siguiente NO está incluido en esta versión del proyecto:

- Integración con pasarelas de pago reales (Wompi, PayU, PSE)
- Envío de notificaciones por email o SMS
- Aplicación móvil nativa
- Dashboard visual con gráficos para reportes
- Sistema de recomendación de eventos
- Integración con redes sociales
- Funcionalidad de reembolsos automatizados
- Chat de soporte en línea
- Sistema de calificaciones y comentarios de eventos
- Aplicación de descuentos y cupones

Estas funcionalidades podrán considerarse para versiones futuras del sistema.

---

## Roles y Responsabilidades

### Desarrollador Principal
**Juan Felipe Huérfano Rúa**
- Diseño de arquitectura
- Implementación de endpoints
- Creación de base de datos
- Pruebas unitarias
- Documentación técnica

### Rol Académico
**Docente de Web Services**
- Revisión de entregas
- Retroalimentación técnica
- Evaluación de cumplimiento de criterios

---

## Métricas de Seguimiento

### Historias de Usuario
- Total de historias: 20
- Historias completadas por sprint
- Tiempo promedio por historia

### Calidad de Código
- Cobertura de pruebas unitarias
- Número de bugs encontrados
- Número de bugs resueltos

### Cumplimiento de Cronograma
- Sprints completados a tiempo
- Historias completadas vs planificadas
- Retrasos y causas

---

## Riesgos Identificados

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Retraso en implementación de módulos | Media | Alto | Priorizar historias críticas primero |
| Problemas con liberación automática de asientos | Media | Medio | Implementar sistema de jobs/cron temprano |
| Complejidad en generación de reportes | Baja | Medio | Dejar para sprint final con tiempo de ajuste |
| Falta de tiempo para pruebas | Media | Alto | Incluir pruebas en cada historia desde inicio |

---

## Aprobación del Alcance

Este documento define el alcance acordado para el proyecto Sistema de Boletería.

**Fecha de definición:** Septiembre 2025

**Estudiante:** Juan Felipe Huérfano Rúa  
**Programa:** Tecnología en Desarrollo de Sistemas Informáticos  
**Institución:** Unidades Tecnológicas de Santander
