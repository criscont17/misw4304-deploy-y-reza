# Autenticación

- Tipo: `Authorization: Bearer <token>`
- **Token estático** configurable (`STATIC_BEARER_TOKEN`, con valor por defecto educativo si no se define en entorno).
- **JWT** opcional: mismo header; el servidor acepta el token si coincide con el estático **o** si es un access token válido firmado con `JWT_SECRET_KEY`.

## Reglas

- Validar en cada request protegida.
- Rechazar si no existe, es inválido o (para JWT) está expirado.

## Documentación del repositorio

Resumen de variables y flujo: `docs/elastic-beanstalk.md` (sección «Bearer: estático o JWT»).
