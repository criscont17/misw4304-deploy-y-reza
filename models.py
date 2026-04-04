"""Modelos de datos para la lista negra global de emails."""

from datetime import datetime
import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID


db = SQLAlchemy()


class Blacklist(db.Model):
    """Modelo principal para almacenar emails bloqueados."""

    __tablename__ = "blacklists"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    app_uuid = db.Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    blocked_reason = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
