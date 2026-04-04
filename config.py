"""Configuración central de la aplicación."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración base cargada desde variables de entorno."""

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "postgresql://postgres:postgres@localhost:5432/blacklist_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me")
