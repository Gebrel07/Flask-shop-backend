from typing import Any

from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token, get_csrf_token

from src.main.usuario import Usuario


class TestClient(FlaskClient):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def login_client(self, id_usuario: int):
        with self.application.app_context():
            usuario = Usuario.query.get(id_usuario)
            token = create_access_token(identity=usuario)

            self.set_cookie(
                self.application.config["JWT_ACCESS_COOKIE_NAME"],
                value=token,
            )

            self.set_cookie(
                self.application.config["JWT_ACCESS_CSRF_COOKIE_NAME"],
                value=get_csrf_token(token),
            )

    def get_x_csrf_header(self):
        cookie = self.get_cookie(
            key=self.application.config["JWT_ACCESS_CSRF_COOKIE_NAME"]
        )
        name = self.application.config["JWT_ACCESS_CSRF_HEADER_NAME"]

        if not cookie:
            return None

        return (name, cookie.value)
