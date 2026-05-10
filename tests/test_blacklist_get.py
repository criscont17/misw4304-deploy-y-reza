"""Pruebas unitarias de GET /blacklists/<email> con el servicio mockeado (sin BD)."""

from unittest.mock import patch


def test_get_blacklist_listed_200(client, auth_headers):
    with patch("app.api.blacklist_resources._service") as mock_svc:
        mock_svc.get_status.return_value = (
            {"blacklisted": True, "blocked_reason": "Fraude"},
            200,
        )
        resp = client.get(
            "/blacklists/fraude@ejemplo.com",
            headers=auth_headers,
        )
    assert resp.status_code == 200
    assert resp.get_json() == {"blacklisted": True, "blocked_reason": "Fraude"}
    mock_svc.get_status.assert_called_once_with("fraude@ejemplo.com")


def test_get_blacklist_not_listed_200(client, auth_headers):
    with patch("app.api.blacklist_resources._service") as mock_svc:
        mock_svc.get_status.return_value = ({"blacklisted": False}, 200)
        resp = client.get(
            "/blacklists/limpio@ejemplo.com",
            headers=auth_headers,
        )
    assert resp.status_code == 200
    assert resp.get_json() == {"blacklisted": False}


def test_get_blacklist_unauthorized_401(client):
    with patch("app.api.blacklist_resources._service") as mock_svc:
        resp = client.get("/blacklists/cualquiera@ejemplo.com")
    assert resp.status_code == 401
    mock_svc.get_status.assert_not_called()


def test_get_blacklist_invalid_bearer_401(client):
    with patch("app.api.blacklist_resources._service") as mock_svc:
        resp = client.get(
            "/blacklists/cualquiera@ejemplo.com",
            headers={"Authorization": "Bearer token-invalido"},
        )
    assert resp.status_code == 401
    mock_svc.get_status.assert_not_called()
