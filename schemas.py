"""Esquemas de serialización para la API de lista negra."""

from flask_marshmallow import Marshmallow

from models import Blacklist


ma = Marshmallow()


class BlacklistSchema(ma.SQLAlchemyAutoSchema):
    """Schema de serialización del modelo Blacklist."""

    class Meta:
        model = Blacklist
        load_instance = True
        include_fk = True
