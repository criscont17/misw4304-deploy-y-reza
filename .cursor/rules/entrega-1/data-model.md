# Modelo de datos

Tabla: blacklist

Campos:
- id (uuid)
- email (string)
- app_uuid (uuid)
- blocked_reason (string)
- ip (string)
- created_at (datetime)

## Reglas

- email único
- registrar IP automáticamente
- fechas en UTC