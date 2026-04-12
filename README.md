# Blacklist API — lista negra global de emails

**misw4304-deploy-y-reza** es un microservicio REST para registrar y consultar emails en una lista negra global. Está pensado para el curso **MISO / DevOps**, con despliegue manual en **AWS** (Elastic Beanstalk) y persistencia en **PostgreSQL**.

**Stack:** Python 3.8+, Flask 3.x, Flask-RESTful, SQLAlchemy, Marshmallow, JWT (Bearer). Las versiones concretas están en `requirements.txt`.

## Inicio rápido

```bash
python -m venv venv
source venv/bin/activate    # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Crea un `.env` en la raíz con al menos `JWT_SECRET_KEY` y `DATABASE_URL` (PostgreSQL). Si omites `DATABASE_URL`, existe un valor por defecto solo para desarrollo local.

```bash
python wsgi.py
```

Servidor por defecto en `http://127.0.0.1:5000`. Alternativa: `flask --app wsgi run`.

## Stack y requisitos

- **Python** 3.8 o superior y **pip**
- **PostgreSQL** (local, RDS u otro proveedor)
- Dependencias: `requirements.txt`

## Despliegue (AWS Elastic Beanstalk)

Resumen:

- Incluye en el paquete **`.ebextensions/`** y **`wsgi.py`**; el contenedor usa `WSGIPath: wsgi:app` (ver `.ebextensions/app.config`).
- Define **`DATABASE_URL`** y **`JWT_SECRET_KEY`** en **Configuration → Software → Environment properties**.

Guía un poco más detallada (WSGI, zip, variables, health, Gunicorn): **[docs/elastic-beanstalk.md](docs/elastic-beanstalk.md)**.

Comando de referencia si usas Gunicorn manualmente:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

## Documentación en `docs/`

| Recurso | Descripción |
|---------|-------------|
| [docs/elastic-beanstalk.md](docs/elastic-beanstalk.md) | Elastic Beanstalk y este repositorio |
| Colección Postman (`docs/blacklist-api.postman_collection.json`) | Requests de ejemplo, precondiciones en la descripción de la colección |

## API (resumen)

Los endpoints de negocio requieren `Authorization: Bearer <token>`. Detalle de códigos y ejemplos: **Postman** en `docs/`.

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| `GET` | `/health` | No | Estado del servicio (`{"status": "ok"}`) |
| `POST` | `/blacklists` | Sí | Alta de email (`email`, `app_uuid`, `blocked_reason` opcional ≤255) |
| `GET` | `/blacklists/<email>` | Sí | Indica si está listado y el motivo |

Ejemplo mínimo de cuerpo para `POST /blacklists`:

```json
{
  "email": "usuario@ejemplo.com",
  "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "blocked_reason": "Opcional"
}
```

## Generar un token JWT (pruebas)

Con el entorno virtual activado:

```bash
python -c "
from app import create_app
from flask_jwt_extended import create_access_token
app = create_app()
app.app_context().push()
print(create_access_token(identity='api-client', expires_delta=False))
"
```

`expires_delta=False` evita expiración; úsalo solo en entornos de prueba.

## Estructura del proyecto

Organización por capas: recursos HTTP delgados (`app/api`), lógica en servicios (`app/services`), modelo y esquemas aparte.

```
├── wsgi.py
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── api/
│   ├── services/
│   ├── models/
│   └── schemas/
├── docs/                    # Postman, guía EB
├── .ebextensions/
├── requirements.txt
├── LICENSE
└── README.md
```

El archivo `.env` no se versiona (ver `.gitignore`).

## Licencia

Ver el archivo `LICENSE` en la raíz del repositorio.
