# AWS Elastic Beanstalk

Elastic Beanstalk es un servicio **PaaS**: subes una versión de tu aplicación (por ejemplo un `.zip` con el código) y AWS aprovisiona o actualiza instancias, balanceador de carga y configuración de entorno según la plataforma elegida (aquí, **Python**).

## Qué hace falta en el artefacto de despliegue

- El código del repositorio, incluido **`wsgi.py`** en la raíz (punto de entrada WSGI).
- La carpeta **`.ebextensions/`** con la configuración del contenedor. En este repo, `app.config` fija el módulo y la aplicación WSGI que debe cargar el contenedor Python de EB.

El valor relevante es **`WSGIPath: wsgi:app`**: el contenedor importa el módulo `wsgi` y usa el objeto Flask llamado `app`. Si cambias el nombre del módulo o del objeto, debes actualizar `WSGIPath` y volver a desplegar.

## Variables de entorno

La aplicación lee al menos:

| Variable | Uso |
|----------|-----|
| `DATABASE_URL` | Cadena de conexión PostgreSQL (también se admite `SQLALCHEMY_DATABASE_URI` como alternativa en código). |
| `JWT_SECRET_KEY` | Secreto para firmar tokens JWT. |

En la consola de AWS: **Elastic Beanstalk → tu entorno → Configuration → Software → Environment properties**. Tras guardar, EB suele aplicar un rolling update; revisa el estado del entorno si el health pasa a degradado.

## Comprobación de salud

El servicio expone **`GET /health`** sin autenticación y responde `{"status": "ok"}`. Puedes usarlo como comprobación rápida tras un despliegue o desde el balanceador si en el futuro configuras un health check HTTP explícito.

## Gunicorn y el puerto

Si ejecutas la app manualmente con Gunicorn (por ejemplo en una máquina local o siguiendo guías de EB), el objetivo WSGI debe coincidir con el del entorno:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

En Elastic Beanstalk el **puerto que escucha el proxy** lo define la plataforma; no asumas que sea `5000` como en `python wsgi.py` en tu máquina. Ajusta pruebas y clientes al host y puerto públicos del entorno.

## Archivo `.ebextensions` incluido

Además de `WSGIPath`, el proyecto declara un fragmento de configuración Apache (`WSGIApplicationGroup %{GLOBAL}`), habitual en plataformas Python sobre Apache para evitar problemas con extensiones nativas cargadas en varios subprocesos. Si cambias de stack de plataforma en AWS, revisa si esa directiva sigue aplicando.

## Referencia oficial

Documentación general de Elastic Beanstalk: [https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html)
