# Imagen base ligera y estable
FROM python:3.11-slim

# Buenas prácticas de Python en contenedor
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Dependencias del sistema (psycopg2-binary y compilación)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias primero (mejor cache de capas)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Puerto de la app (Gunicorn)
EXPOSE 8000

# Healthcheck interno del contenedor
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health').read()"

## ==========================================
## CONFIGURACIÓN DE NEW RELIC
## ==========================================
ENV NEW_RELIC_APP_NAME="blacklist-api-prod" \
    NEW_RELIC_LOG="stdout" \
    NEW_RELIC_LOG_LEVEL="info" \
    NEW_RELIC_DISTRIBUTED_TRACING_ENABLED="true"

# Envolvemos el arranque con el agente de New Relic
ENTRYPOINT ["newrelic-admin", "run-program"]

# Tu comando original de arranque ahora pasará a través del ENTRYPOINT
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]