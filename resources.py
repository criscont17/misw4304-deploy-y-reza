"""Recursos REST para la API de lista negra."""

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from models import Blacklist, db
from schemas import BlacklistCreateSchema

create_schema = BlacklistCreateSchema()


class BlacklistResource(Resource):
    """Maneja operaciones sobre la colección de lista negra."""

    @jwt_required()
    def post(self):
        """Agrega un email a la lista negra global."""
        json_data = request.get_json(silent=True)
        if not json_data:
            return {"message": "El body debe ser JSON válido"}, 400

        try:
            data = create_schema.load(json_data)
        except ValidationError as err:
            return {"message": "Errores de validación", "errors": err.messages}, 400

        existing = Blacklist.query.filter_by(email=data["email"]).first()
        if existing:
            return {"message": "El email ya se encuentra en la lista negra"}, 400

        entry = Blacklist(
            email=data["email"],
            app_uuid=data["app_uuid"],
            blocked_reason=data.get("blocked_reason"),
            ip_address=request.remote_addr or "0.0.0.0",
        )
        db.session.add(entry)
        db.session.commit()

        return {"message": "Email agregado a la lista negra exitosamente"}, 201


class BlacklistDetailResource(Resource):
    """Maneja operaciones sobre un email específico en la lista negra."""

    @jwt_required()
    def get(self, email):
        """Consulta si un email está en la lista negra global."""
        entry = Blacklist.query.filter_by(email=email).first()

        if entry:
            return {
                "blacklisted": True,
                "blocked_reason": entry.blocked_reason or "",
            }, 200

        return {"blacklisted": False}, 200
