"""Configuración central de la aplicación."""

import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def _env_stripped(key: str, default: Optional[str] = None) -> Optional[str]:
    """Lee una variable de entorno y elimina espacios accidentales al inicio/final."""
    value = os.getenv(key, default)
    if value is None:
        return None
    stripped = value.strip()
    return stripped if stripped else None


def _static_bearer_token_from_env() -> Optional[str]:
    """
    Token Bearer fijo opcional. Si STATIC_BEARER_TOKEN no está definido, se usa un
    valor por defecto educativo. Si está definido pero vacío (tras trim), se desactiva
    el modo estático y solo se aceptan JWT.
    """
    raw = os.getenv("STATIC_BEARER_TOKEN")
    if raw is None:
        return "misw4304-static-bearer"
    stripped = raw.strip()
    return stripped if stripped else None


class Config:
    """Configuración base cargada desde variables de entorno."""

    #: Si es True, `create_app` no ejecuta `db.create_all()` (pruebas unitarias sin DDL).
    SKIP_DB_CREATE_ALL = False
    SQLALCHEMY_DATABASE_URI = (
        _env_stripped("DATABASE_URL")
        or _env_stripped("SQLALCHEMY_DATABASE_URI")
        or "postgresql://postgres:postgres@localhost:5432/blacklist_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_SECRET_KEY = _env_stripped("JWT_SECRET_KEY") or "change-me"
    STATIC_BEARER_TOKEN = _static_bearer_token_from_env()


class TestingConfig(Config):
    """Configuración para pruebas: sin crear esquema en BD; URI dummy para SQLAlchemy."""

    TESTING = True
    SKIP_DB_CREATE_ALL = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "test-jwt-secret-key"
    STATIC_BEARER_TOKEN = "test-static-bearer-token"
