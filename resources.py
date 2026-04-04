"""Recursos REST para la API de lista negra."""

from flask_jwt_extended import jwt_required
from flask_restful import Resource


class BlacklistResource(Resource):
    """Maneja operaciones sobre la colección de lista negra."""

    @jwt_required()
    def post(self):
        """Crea un registro en la lista negra (pendiente de implementación)."""
        return {
            "message": "Endpoint POST /blacklists listo",
            "status": "pending_implementation",
        }, 202


class BlacklistDetailResource(Resource):
    """Maneja operaciones sobre un email específico en la lista negra."""

    @jwt_required()
    def get(self, email):
        """Obtiene un registro por email (pendiente de implementación)."""
        return {
            "message": "Endpoint GET /blacklists/<email> listo",
            "email": email,
            "status": "pending_implementation",
        }, 200
