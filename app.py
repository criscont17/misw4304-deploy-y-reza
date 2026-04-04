"""Punto de entrada de la aplicación Flask."""

from flask import Flask, jsonify
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


@jwt.unauthorized_loader
def missing_token_callback(error_string):
    return jsonify({"message": "Token de autorización faltante"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    return jsonify({"message": "Token inválido o expirado"}), 401


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "El token ha expirado"}), 401


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
