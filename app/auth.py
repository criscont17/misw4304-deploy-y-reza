"""Autenticación Bearer: token estático (predefinido) o JWT."""

import secrets
from functools import wraps
from typing import Any, Callable, Optional, Tuple

from flask import current_app, request
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import ExpiredSignatureError, PyJWTError


def _parse_bearer_token() -> Tuple[Optional[str], Optional[str]]:
    """
    Devuelve (None, mensaje_error) si falta o es inválido el header;
    (token_str, None) si hay Bearer con valor.
    """
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return None, "Token de autorización faltante"
    token = auth[7:].strip()
    if not token:
        return None, "Token de autorización faltante"
    return token, None


def _static_token_accepted(token: str) -> bool:
    static = current_app.config.get("STATIC_BEARER_TOKEN")
    if not static:
        return False
    if len(token) != len(static):
        return False
    return secrets.compare_digest(token, static)


def bearer_auth_required(fn: Callable[..., Any]) -> Callable[..., Any]:
    """
    Acepta Authorization: Bearer <valor> donde valor es:
    - el token estático configurado (STATIC_BEARER_TOKEN), o
    - un JWT válido firmado con JWT_SECRET_KEY.
    """

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any):
        token, err = _parse_bearer_token()
        if err:
            return {"message": err}, 401

        if _static_token_accepted(token):
            return fn(*args, **kwargs)

        try:
            verify_jwt_in_request()
        except ExpiredSignatureError:
            return {"message": "El token ha expirado"}, 401
        except (JWTExtendedException, PyJWTError):
            return {"message": "Token inválido o expirado"}, 401

        return fn(*args, **kwargs)

    return wrapper
