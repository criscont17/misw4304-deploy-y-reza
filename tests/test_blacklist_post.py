"""Pruebas unitarias de POST /blacklists con el servicio mockeado (sin BD)."""

from unittest.mock import patch
from uuid import UUID

import pytest


@pytest.fixture
def valid_body():
    return {
        "email": "usuario@ejemplo.com",
        "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
        "blocked_reason": "Prueba",
    }


def test_post_blacklist_success_201(client, auth_headers, valid_body):
    with patch("app.api.blacklist_resources._service") as mock_svc:
        mock_svc.add_email.return_value = (
            {"message": "Email agregado a la lista negra exitosamente"},
            201,
        )
        resp = client.post(
            "/blacklists",
            json=valid_body,
            headers={**auth_headers, "Content-Type": "application/json"},
        )
    assert resp.status_code == 201
    assert resp.get_json() == {"message": "Email agregado a la lista negra exitosamente"}
    mock_svc.add_email.assert_called_once()
    call_kw = mock_svc.add_email.call_args.kwargs
    assert call_kw["email"] == valid_body["email"]
    assert call_kw["app_uuid"] == UUID(valid_body["app_uuid"])
    assert call_kw["blocked_reason"] == valid_body["blocked_reason"]
    assert "ip_address" in call_kw


def test_post_blacklist_duplicate_400(client, auth_headers, valid_body):
    with patch("app.api.blacklist_resources._service") as mock_svc:
        mock_svc.add_email.return_value = (
            {"message": "El email ya se encuentra en la lista negra"},
            400,
        )
        resp = client.post(
            "/blacklists",
            json=valid_body,
            headers={**auth_headers, "Content-Type": "application/json"},
        )
    assert resp.status_code == 400
    assert resp.get_json() == {"message": "El email ya se encuentra en la lista negra"}


def test_post_blacklist_validation_invalid_email_400(client, auth_headers):
    with patch("app.api.blacklist_resources._service") as mock_svc:
        resp = client.post(
            "/blacklists",
            json={
                "email": "no-es-email",
                "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
            },
            headers={**auth_headers, "Content-Type": "application/json"},
        )
    assert resp.status_code == 400
    body = resp.get_json()
    assert body.get("message") == "Errores de validación"
    assert "errors" in body
    mock_svc.add_email.assert_not_called()


def test_post_blacklist_invalid_json_body_400(client, auth_headers):
    with patch("app.api.blacklist_resources._service") as mock_svc:
        resp = client.post(
            "/blacklists",
            data="",
            headers={**auth_headers, "Content-Type": "application/json"},
        )
    assert resp.status_code == 400
    assert resp.get_json() == {"message": "El body debe ser JSON válido"}
    mock_svc.add_email.assert_not_called()


def test_post_blacklist_unauthorized_401(client, valid_body):
    with patch("app.api.blacklist_resources._service") as mock_svc:
        resp = client.post(
            "/blacklists",
            json=valid_body,
            headers={"Content-Type": "application/json"},
        )
    assert resp.status_code == 401
    mock_svc.add_email.assert_not_called()
