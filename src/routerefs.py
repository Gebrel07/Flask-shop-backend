from flask import Flask

from .main.auth import auth_bp
from .main.produtos import produtos_bp
from .main.usuario import usuario_bp


def register_blueprints(app: Flask):
    app.register_blueprint(auth_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(usuario_bp)
    return app
