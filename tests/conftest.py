"""Fixtures compartidas: app de prueba sin DDL ni PostgreSQL."""

import pytest

from app import create_app
from app.config import TestingConfig


@pytest.fixture
def app():
    """Aplicación Flask con servicio de BD desactivado en el arranque."""
    return create_app(TestingConfig)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(app):
    token = app.config["STATIC_BEARER_TOKEN"]
    return {"Authorization": f"Bearer {token}"}
