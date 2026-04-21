"""Aplicación Flask: factory y registro de extensiones y rutas."""

from flask import Flask
from flask_restful import Api

from app.api.blacklist_resources import BlacklistDetailResource, BlacklistResource
from app.config import Config
from app.extensions import db, jwt, ma


def create_app(config_class=Config):
    """App Factory para crear y configurar la aplicación."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    api = Api(app)
    api.add_resource(BlacklistResource, "/blacklists")
    api.add_resource(BlacklistDetailResource, "/blacklists/<string:email>")

    @app.route("/health", methods=["GET"])
    def health_check():
        return {"status": "ok"}, 200

    with app.app_context():
        from app.models import Blacklist  # noqa: F401

        db.create_all()

    return app
