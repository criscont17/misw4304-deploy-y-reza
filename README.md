# # misw4304-deploy-y-reza Blacklist API - Lista Negra Global de Emails

Microservicio REST para gestionar una lista negra global de emails. Permite agregar emails a la lista negra y consultar si un email se encuentra bloqueado.

## Tecnologías

- Python 3.8+
- Flask 1.1.4 + Flask-RESTful
- Flask-SQLAlchemy + PostgreSQL (Supabase)
- Flask-Marshmallow (validación y serialización)
- Flask-JWT-Extended (autenticación Bearer Token)

## Requisitos previos

- Python 3.8 o superior
- PostgreSQL (local o Supabase)
- pip

## Instalación y ejecución local

### 1. Crear y activar entorno virtual

```bash
python -m venv venv
```

Windows (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
JWT_SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_db
```

`DATABASE_URL` apunta a la base de datos principal (por ejemplo, Supabase). Si no se define, se usa `SQLALCHEMY_DATABASE_URI` como fallback para desarrollo local.

### 4. Ejecutar la aplicación

```bash
python app.py
```

El servidor arranca en `http://localhost:5000`.

## Despliegue en producción (AWS Elastic Beanstalk)

Al crear el entorno en Elastic Beanstalk y subir el `.zip` del proyecto, configurar el **start command**:

```
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

Gunicorn ya está incluido en `requirements.txt`. Elastic Beanstalk usa el puerto **8000** por defecto.

Configurar las variables de entorno (`DATABASE_URL`, `JWT_SECRET_KEY`) desde la consola de AWS en **Configuration > Software > Environment properties**.

## Endpoints

Todos los endpoints protegidos requieren el header `Authorization: Bearer <token>`.

### Health Check

```
GET /health
```

No requiere autenticación. Respuesta:

```json
{"status": "ok"}
```

### Agregar email a la lista negra

```
POST /blacklists
```

Headers:

```
Authorization: Bearer <token>
Content-Type: application/json
```

Body:

```json
{
  "email": "usuario@ejemplo.com",
  "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "blocked_reason": "Motivo opcional (máx. 255 caracteres)"
}
```

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| email | String | Sí | Email a bloquear |
| app_uuid | UUID | Sí | ID de la aplicación cliente |
| blocked_reason | String | No | Motivo del bloqueo (máx. 255 chars) |

Respuestas:

- `201` - Email agregado exitosamente
- `400` - Email duplicado o datos inválidos
- `401` - Token faltante o inválido

### Consultar email en la lista negra

```
GET /blacklists/<email>
```

Headers:

```
Authorization: Bearer <token>
```

Respuestas:

- `200` si está en la lista negra:

```json
{"blacklisted": true, "blocked_reason": "Motivo del bloqueo"}
```

- `200` si no está:

```json
{"blacklisted": false}
```

- `401` - Token faltante o inválido

## Generar un token JWT

Con el entorno virtual activado:

```bash
python -c "from app import create_app; from flask_jwt_extended import create_access_token; app = create_app(); app.app_context().push(); print(create_access_token(identity='api-client', expires_delta=False))"
```

El parámetro `expires_delta=False` genera un token sin expiración.

## Estructura del proyecto

```
├── app.py              # App Factory y punto de entrada
├── config.py           # Configuración desde variables de entorno
├── models.py           # Modelo Blacklist (SQLAlchemy)
├── schemas.py          # Schemas de validación (Marshmallow)
├── resources.py        # Endpoints REST
├── requirements.txt    # Dependencias pinneadas
├── .env                # Variables de entorno (no versionado)
└── README.md
```
