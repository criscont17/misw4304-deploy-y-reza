# Blacklist API — lista negra global de emails

**misw4304-deploy-y-reza** es un microservicio REST para registrar y consultar emails en una lista negra global. Está pensado para el curso **MISO / DevOps**, con despliegue en **AWS** (Elastic Beanstalk) y persistencia en **PostgreSQL**.

**Stack:** Python 3.8+, Flask 3.x, Flask-RESTful, SQLAlchemy, Marshmallow, autenticación **Bearer** (token estático opcional o JWT). Las versiones concretas están en `requirements.txt`.

## Inicio rápido

```bash
python -m venv venv
source venv/bin/activate    # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Crea un `.env` en la raíz con al menos `DATABASE_URL` (PostgreSQL). Opcional: `JWT_SECRET_KEY` y `STATIC_BEARER_TOKEN` (Bearer estático o solo JWT; ver **[docs/elastic-beanstalk.md](docs/elastic-beanstalk.md)**).

```bash
python wsgi.py
```

Servidor por defecto en `http://127.0.0.1:5000`. Alternativa: `flask --app wsgi run`.

### Token Bearer estático (pruebas locales)

Si **no** defines `STATIC_BEARER_TOKEN` en `.env`, la API usa por defecto el token fijo `misw4304-static-bearer`. Para `POST /blacklists` y `GET /blacklists/<email>` incluye el header:

```http
Authorization: Bearer misw4304-static-bearer
```

Si defines `STATIC_BEARER_TOKEN` en `.env`, usa ese valor en el header en su lugar. Si la variable existe pero está vacía (solo espacios), el modo estático se desactiva y solo se aceptan JWT; detalle en **[docs/elastic-beanstalk.md](docs/elastic-beanstalk.md)**. La colección Postman en `docs/blacklist-api.postman_collection.json` trae la variable `token` con el mismo valor por defecto.

## Stack y requisitos

- **Python** 3.8 o superior y **pip**
- **PostgreSQL** (local, RDS u otro proveedor)
- Dependencias: `requirements.txt` (incluye `pytest` para las pruebas unitarias).

## Pruebas unitarias

Tras `pip install -r requirements.txt`, ejecuta **`pytest tests/ -v`**. Los tests **mockean** el servicio de lista negra y no requieren PostgreSQL.

## Despliegue (AWS Elastic Beanstalk)

Resumen:

- Incluye en el paquete **`.ebextensions/`** y **`wsgi.py`**; el contenedor usa `WSGIPath: wsgi:app` (ver `.ebextensions/app.config`).
- Define **`DATABASE_URL`**, **`JWT_SECRET_KEY`** y **`STATIC_BEARER_TOKEN`** según necesites (Bearer estático y/o JWT; ver **[docs/elastic-beanstalk.md](docs/elastic-beanstalk.md)**) en **Configuration → Software → Environment properties**.

Guía (WSGI, zip, variables, health, Gunicorn, Bearer): **[docs/elastic-beanstalk.md](docs/elastic-beanstalk.md)**.

Comando de referencia si usas Gunicorn manualmente:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

## CI/CD en AWS (resumen)

El flujo automatizado recomendado para este repositorio es:

`CodePipeline -> CodeBuild -> Amazon ECR -> Elastic Beanstalk`

- **CodeBuild** usa `buildspec.yml` para ejecutar pruebas (`pytest`), construir imagen Docker y publicarla en ECR.
- **ECR** almacena las imagenes con tags `latest` y hash corto de commit.
- **Elastic Beanstalk** despliega la imagen publicada usando `Dockerrun.aws.json`.

Guia detallada: **[docs/continuous-integration.md](docs/continuous-integration.md)**.

## Documentación en `docs/`

| Recurso | Descripción |
|---------|-------------|
| [docs/elastic-beanstalk.md](docs/elastic-beanstalk.md) | Elastic Beanstalk, variables de entorno y autenticación Bearer (estático / JWT) |
| [docs/continuous-integration.md](docs/continuous-integration.md) | Integracion continua y despliegue en AWS con ECR, CodeBuild, CodePipeline y Elastic Beanstalk |
| Colección Postman (`docs/blacklist-api.postman_collection.json`) | Requests de ejemplo, variable `token` por defecto alineada con el Bearer estático |

## API (resumen)

Los endpoints de negocio requieren `Authorization: Bearer <token>` (**estático** o **JWT**; token estático por defecto en **Token Bearer estático** más arriba; despliegue y variables: **[docs/elastic-beanstalk.md](docs/elastic-beanstalk.md)**). Códigos y ejemplos: **Postman** en `docs/`.

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

## Generar un token JWT (opcional)

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
│   ├── auth.py
│   ├── config.py
│   ├── extensions.py
│   ├── api/
│   ├── services/
│   ├── models/
│   └── schemas/
├── tests/                   # Pytest (mocks; sin PostgreSQL)
├── docs/                    # Postman, guía EB
├── .ebextensions/
├── pytest.ini
├── requirements.txt
├── LICENSE
└── README.md
```

El archivo `.env` no se versiona (ver `.gitignore`).

## Licencia

Ver el archivo `LICENSE` en la raíz del repositorio.
