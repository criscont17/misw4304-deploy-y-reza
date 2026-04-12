"""Esquemas de serialización para la API de lista negra."""

from marshmallow import fields, validate

from app.extensions import ma
from app.models import Blacklist


class BlacklistSchema(ma.SQLAlchemyAutoSchema):
    """Schema de serialización del modelo Blacklist."""

    class Meta:
        model = Blacklist
        load_instance = True
        include_fk = True


class BlacklistCreateSchema(ma.Schema):
    """Schema de validación para el POST /blacklists."""

    email = fields.Email(required=True)
    app_uuid = fields.UUID(required=True)
    blocked_reason = fields.String(
        load_default=None,
        validate=validate.Length(max=255),
    )
