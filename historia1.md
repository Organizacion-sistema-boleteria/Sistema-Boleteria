[HU-001] Registrar Usuario en el Sistema
📖 Historia de Usuario
Como usuario nuevo
Quiero registrarme en el sistema proporcionando mis datos personales
Para poder comprar boletos para eventos
🔁 Flujo Esperado

El usuario accede al formulario de registro en la aplicación
El usuario completa los campos obligatorios: nombre, email, teléfono y contraseña
El sistema valida que el email no esté registrado previamente en la base de datos
El sistema encripta la contraseña usando un algoritmo de hash seguro
El sistema asigna automáticamente el rol de CLIENTE al nuevo usuario
El sistema registra la fecha y hora actual del registro
El sistema establece el estado del usuario como ACTIVO
El sistema devuelve una confirmación con los datos del usuario creado

✅ Criterios de Aceptación
1. Estructura y lógica del servicio

 Se expone un endpoint POST /api/usuarios que permite el registro público
 Se valida que el campo email tenga un formato válido antes de procesarlo
 Se verifica que el email no exista previamente en la tabla usuario
 La contraseña se almacena encriptada en el campo password_hash
 El campo rol se establece automáticamente como CLIENTE
 El campo fecha_registro se completa con la fecha y hora actual
 El campo estado se establece como ACTIVO por defecto

2. Estructura de la información

 Se responde con la siguiente estructura en JSON:

json{
  "success": true,
  "message": "Usuario creado exitosamente",
  "data": {
    "usuarioId": 1,
    "nombre": "Juan Pérez",
    "email": "juan@email.com",
    "telefono": "3001234567",
    "rol": "CLIENTE",
    "fechaRegistro": "2025-09-08T15:30:00Z",
    "estado": "ACTIVO"
  }
}

 Si el email ya existe, el backend retorna:

json{
  "success": false,
  "message": "El correo electrónico ya está registrado",
  "error": {
    "code": 409,
    "details": "El email ya existe en el sistema"
  }
}
🔧 Notas Técnicas
Endpoint – Registrar Usuario

Método HTTP: POST
Ruta: /api/usuarios
Acceso: Público
Entidad: Usuario
Tabla BD: usuario

Campos de la tabla usuario

usuario_id (PK, Entero)
nombre (Texto, No nulo)
email (Texto, Único, No nulo)
telefono (Texto)
password_hash (Texto, No nulo)
rol (Texto: CLIENTE, ORGANIZADOR, ADMINISTRADOR)
fecha_registro (Fecha/Hora)
estado (Texto: ACTIVO, INACTIVO, SUSPENDIDO)

📤 Ejemplo de Respuesta JSON
json{
  "success": true,
  "message": "Usuario creado exitosamente",
  "data": {
    "usuarioId": 1,
    "nombre": "Juan Pérez",
    "email": "juan@email.com",
    "telefono": "3001234567",
    "rol": "CLIENTE",
    "fechaRegistro": "2025-09-08T15:30:00Z",
    "estado": "ACTIVO"
  }
}
🧪 Requisitos de Pruebas
Casos de Prueba Funcional
Caso 1: Registro exitoso de nuevo usuario

Precondición: El email proporcionado no existe en la tabla usuario
Acción: Ejecutar el endpoint POST /api/usuarios con nombre, email, telefono y contraseña válidos
Resultado esperado:

Código HTTP 201 Created
Se crea un nuevo registro en la tabla usuario
El campo password_hash contiene la contraseña encriptada
El campo rol tiene el valor CLIENTE
El campo estado tiene el valor ACTIVO
El campo fecha_registro contiene la fecha y hora actual



Caso 2: Intento de registro con email duplicado

Precondición: El email ya existe en la tabla usuario
Acción: Ejecutar el endpoint POST /api/usuarios con un email que ya está registrado
Resultado esperado:

Código HTTP 409 Conflict
Campo success = false
Campo mensaje contiene el texto: "El correo electrónico ya está registrado"
No se crea ningún registro nuevo en la base de datos



Caso 3: Validación de formato de email

Precondición: Se envía un email con formato inválido
Acción: Ejecutar el endpoint POST /api/usuarios con email sin formato válido
Resultado esperado:

Código HTTP 400 Bad Request
Campo success = false
Campo mensaje contiene el texto: "El formato del email no es válido"



Caso 4: Campos obligatorios faltantes

Precondición: No se envían todos los campos requeridos
Acción: Ejecutar el endpoint POST /api/usuarios sin el campo nombre o email o contraseña
Resultado esperado:

Código HTTP 400 Bad Request
Campo success = false
Campo mensaje especifica qué campos son obligatorios



Caso 5: Error de conexión a base de datos

Precondición: La base de datos no está disponible
Acción: Ejecutar el endpoint bajo condiciones simuladas de fallo de BD
Resultado esperado:

Código HTTP 500 Internal Server Error
Campo success = false
Campo mensaje contiene el texto: "No fue posible registrar el usuario"



✅ Definición de Hecho
Alcance Funcional

 El endpoint POST /api/usuarios crea usuarios correctamente en la tabla usuario
 La validación de email único funciona correctamente
 La encriptación de contraseña está implementada
 El rol CLIENTE se asigna automáticamente
 El estado ACTIVO se establece por defecto
 La respuesta JSON cumple con el formato estandarizado definido

Pruebas Completadas

 Se ejecutaron pruebas unitarias para validación de formato de email
 Se ejecutaron pruebas para verificar duplicidad de email
 Se probó la encriptación correcta de la contraseña
 Se cubrieron los casos de error y validación de campos obligatorios
 Las pruebas funcionales están documentadas y aprobadas

Documentación Técnica

 Endpoint documentado en Swagger o herramienta similar
 Se describe el propósito del servicio de registro
 Se documentan los campos de entrada obligatorios y opcionales
 Se incluye ejemplo de request body
 Se incluye ejemplo de respuesta exitosa
 Se incluyen ejemplos de respuestas de error
 Se documentan los códigos HTTP utilizados

Manejo de Errores

 Se devuelve código HTTP 409 cuando el email ya existe
 Se devuelve código HTTP 400 cuando faltan campos obligatorios o tienen formato inválido
 Se devuelve código HTTP 500 cuando hay error en el servidor o base de datos
 El campo mensaje en el JSON incluye texto descriptivo del error
