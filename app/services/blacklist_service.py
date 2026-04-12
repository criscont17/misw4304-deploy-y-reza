"""Lógica de negocio de la lista negra."""

from typing import Any, Dict, Optional, Tuple
from uuid import UUID

from app.extensions import db
from app.models import Blacklist


class BlacklistService:
    """Operaciones sobre emails en lista negra."""

    def add_email(
        self,
        email: str,
        app_uuid: UUID,
        blocked_reason: Optional[str],
        ip_address: str,
    ) -> Tuple[Dict[str, Any], int]:
        """Registra un email en la lista negra. Respuestas compatibles con la API actual."""
        existing = Blacklist.query.filter_by(email=email).first()
        if existing:
            return {"message": "El email ya se encuentra en la lista negra"}, 400

        entry = Blacklist(
            email=email,
            app_uuid=app_uuid,
            blocked_reason=blocked_reason,
            ip_address=ip_address,
        )
        db.session.add(entry)
        db.session.commit()

        return {"message": "Email agregado a la lista negra exitosamente"}, 201

    def get_status(self, email: str) -> Tuple[Dict[str, Any], int]:
        """Consulta si un email está listado. Misma forma de respuesta que antes."""
        entry = Blacklist.query.filter_by(email=email).first()

        if entry:
            return {
                "blacklisted": True,
                "blocked_reason": entry.blocked_reason or "",
            }, 200

        return {"blacklisted": False}, 200
