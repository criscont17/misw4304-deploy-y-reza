# Diseño API REST

## Endpoint 1: POST /blacklists

### Descripción
- Ninguna.

### Parámetros de autorización
- Bearer Token.

### Entrada
- email: string
- app_uuid: uuid
- blocked_reason: string (opcional, max 255)

### Salida
- application/json. Un mensaje de confirmación notificando si la cuenta pudo o no ser creada.

---

## Endpoint 2: GET /blacklists/<email>

### Descripción
- Permite saber si un email está en la lista negra global de la organización o no, y el motivo
por el que fue agregado a la lista negra.

### Parámetros de autorización
- Bearer Token.

### Entrada
- Ninguno.

### Salida
- blacklisted: boolean
- blocked_reason: string

