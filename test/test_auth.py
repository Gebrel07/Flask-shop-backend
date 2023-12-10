from flask import Flask

from src.extensions import db
from src.main.usuario import Usuario
from src.main.usuario.usr import UserHandler

from .custom_client import TestClient

EMAIL = "teste123@teste.com"
SENHA = "teste123"


def test_login_user(app: Flask, client: TestClient):
    __setup_user(app=app)

    resp = client.post("/auth/login", json={"email": EMAIL, "senha": SENHA})

    assert resp is not None
    assert resp.status_code == 200
    assert resp.json["ok"] is True  # type: ignore

    __teardown_user(app=app)


def test_register_user(app: Flask, client: TestClient):
    __teardown_user(app=app)

    resp = client.post(
        "/auth/register", json={"nome": "teste", "email": EMAIL, "senha": SENHA}
    )

    assert resp is not None
    assert resp.status_code == 200
    assert resp.json["ok"] is True  # type: ignore

    __teardown_user(app=app)


def __setup_user(app: Flask):
    with app.app_context():
        handler = UserHandler()

        usuario = Usuario.query.filter_by(email=EMAIL).first()
        if usuario:
            db.session.delete(usuario)
            db.session.commit()

        user = handler.criar_usuario(nome="Teste", email=EMAIL, senha=SENHA)

    return user


def __teardown_user(app: Flask):
    with app.app_context():
        usuario = Usuario.query.filter_by(email=EMAIL).first()
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
