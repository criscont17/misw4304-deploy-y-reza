"""Recursos REST para la API de lista negra."""

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app.auth import bearer_auth_required
from app.schemas import BlacklistCreateSchema
from app.services import BlacklistService

create_schema = BlacklistCreateSchema()
_service = BlacklistService()


class BlacklistResource(Resource):
    """Maneja operaciones sobre la colección de lista negra."""

    @bearer_auth_required
    def post(self):
        """Agrega un email a la lista negra global."""
        json_data = request.get_json(silent=True)
        if not json_data:
            return {"message": "El body debe ser JSON válido"}, 400

        try:
            data = create_schema.load(json_data)
        except ValidationError as err:
            return {"message": "Errores de validación", "errors": err.messages}, 400

        body, status = _service.add_email(
            email=data["email"],
            app_uuid=data["app_uuid"],
            blocked_reason=data.get("blocked_reason"),
            ip_address=request.remote_addr or "0.0.0.0",
        )
        return body, status


class BlacklistDetailResource(Resource):
    """Maneja operaciones sobre un email específico en la lista negra."""

    @bearer_auth_required
    def get(self, email):
        """Consulta si un email está en la lista negra global."""
        body, status = _service.get_status(email)
        return body, status
