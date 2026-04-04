"""Punto de entrada de la aplicación Flask."""

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from config import Config
from models import db
from resources import BlacklistDetailResource, BlacklistResource
from schemas import ma


jwt = JWTManager()


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

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
