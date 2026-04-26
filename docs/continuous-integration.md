# Integracion continua y despliegue en AWS

Este documento describe el flujo de CI/CD del proyecto usando Amazon ECR, AWS CodeBuild, AWS CodePipeline y AWS Elastic Beanstalk, tomando como referencia `Dockerfile`, `buildspec.yml` y `Dockerrun.aws.json`.

## Objetivo

Automatizar la validacion, construccion y publicacion de la imagen Docker de la API para desplegar versiones trazables en Elastic Beanstalk.

## Flujo de alto nivel

`CodePipeline -> CodeBuild -> Amazon ECR -> Elastic Beanstalk`

1. Un cambio en el repositorio activa el pipeline.
2. CodeBuild ejecuta pruebas unitarias y construye la imagen Docker.
3. CodeBuild publica la imagen en ECR con dos tags: `latest` y el hash corto del commit.
4. Elastic Beanstalk despliega la imagen desde ECR usando `Dockerrun.aws.json`.

## Amazon ECR

### Repositorio de imagen

El proyecto usa el nombre de repositorio `blacklists-api` (variable `IMAGE_REPO_NAME` en `buildspec.yml`).

URI base esperada:

`<AWS_ACCOUNT_ID>.dkr.ecr.<AWS_DEFAULT_REGION>.amazonaws.com/blacklists-api`

### Estrategia de versionado (tags)

Segun `buildspec.yml`, se generan y publican dos tags:

- `latest`: representa la version mas reciente construida.
- `<SHORT_COMMIT_TAG>`: primeros 7 caracteres de `CODEBUILD_RESOLVED_SOURCE_VERSION`.

Esta estrategia permite despliegue rapido (`latest`) y trazabilidad exacta por commit (tag corto).

## AWS CodeBuild

El archivo `buildspec.yml` define estas fases:

### install

- Usa runtime de Python 3.11.
- Instala dependencias del proyecto con `pip install -r requirements.txt`.

### pre_build

- Ejecuta pruebas unitarias: `pytest tests/ -v`.
- Autentica Docker contra ECR con `aws ecr get-login-password`.
- Calcula variables de versionado:
  - `SHORT_COMMIT_TAG`
  - `IMAGE_URI`

### build

- Construye la imagen con el `Dockerfile` del repositorio.
- Aplica tags `latest` y `SHORT_COMMIT_TAG`.

### post_build

- Hace `docker push` de ambas etiquetas a ECR.
- Deja listas las imagenes para despliegue.

## AWS CodePipeline

Configuracion recomendada de etapas para este repositorio:

1. **Source**: origen en repositorio Git.
2. **Build**: proyecto CodeBuild que usa `buildspec.yml`.
3. **Deploy**: despliegue a Elastic Beanstalk consumiendo `Dockerrun.aws.json`.

### Variables y parametros que deben estar alineados

- `AWS_ACCOUNT_ID`
- `AWS_DEFAULT_REGION`
- `IMAGE_REPO_NAME`
- Tag de imagen usado en `Dockerrun.aws.json`

Si estos valores no coinciden entre CodeBuild, ECR y Elastic Beanstalk, el despliegue fallara por imagen no encontrada o permisos insuficientes.

## AWS Elastic Beanstalk

### Artefacto de despliegue de contenedor

`Dockerrun.aws.json` (version 1) define:

- Imagen en ECR a desplegar (`Image.Name`).
- Politica de actualizacion de imagen (`Image.Update: true`).
- Puerto de contenedor (`ContainerPort: 8000`).

Actualmente el archivo usa placeholders:

- `AWS_ACCOUNT_ID`
- `AWS_ECR_IMAGE_TAG`

En cada despliegue debes reemplazar esos valores por los reales de cuenta y tag.

## Relacion con los archivos del repositorio

### `Dockerfile`

- Base `python:3.11-slim`.
- Instala dependencias del sistema y de Python.
- Expone puerto `8000`.
- Define `HEALTHCHECK` contra `/health`.
- Arranca con Gunicorn en `wsgi:app`.

### `buildspec.yml`

- Ejecuta pruebas.
- Construye y etiqueta imagen.
- Publica imagen en ECR.

### `Dockerrun.aws.json`

- Instruye a Elastic Beanstalk para descargar y ejecutar la imagen desde ECR.

## Checklist operativo

1. Crear repositorio ECR `blacklists-api`.
2. Asignar permisos IAM a CodeBuild para:
   - Login en ECR.
   - Push de imagenes.
   - Lectura de fuentes y escritura de logs.
3. Configurar variables de entorno de build:
   - `AWS_ACCOUNT_ID`
   - `AWS_DEFAULT_REGION`
   - `IMAGE_REPO_NAME`
4. Garantizar que `Dockerrun.aws.json` apunte al tag correcto.
5. Verificar en Elastic Beanstalk:
   - Estado del entorno en verde.
   - Endpoint `GET /health` respondiendo `{"status": "ok"}`.
