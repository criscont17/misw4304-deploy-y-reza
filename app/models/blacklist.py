"""Modelo de datos para la lista negra global de emails."""

from sqlalchemy import func, text
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db


class Blacklist(db.Model):
    """Modelo principal para almacenar emails bloqueados."""

    __tablename__ = "blacklists"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    app_uuid = db.Column(UUID(as_uuid=True), nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(45), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
    )
