from flask import url_for
from flask_jwt_extended import create_access_token, get_csrf_token

from src.extensions import bcrypt, db

from .usuario import Usuario


class UserHandler:
    def __init__(self) -> None:
        self.default_img = "default_user.png"

    def get_user_json(self, usuario: Usuario):
        user_obj = {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "profile_pic": url_for(
                "static", filename=self.default_img, _external=True
            ),
        }
        return user_obj

    def criar_usuario(self, nome: str, email: str, senha: str):
        pw_hash = bcrypt.generate_password_hash(password=senha)

        new_user = Usuario(nome=nome, email=email, senha=pw_hash)  # type: ignore

        db.session.add(new_user)
        db.session.commit()

        return new_user

    def validar_login(self, email: str, senha: str) -> Usuario | None:
        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            return None

        pw_validated = bcrypt.check_password_hash(
            pw_hash=usuario.senha, password=senha
        )

        if not pw_validated:
            return None

        return usuario

    def login_user(self, email: str, senha: str, img_base_url: str):
        """Returns:
        dict: {
            "ok": bool,
            "msg": str,
            "access_token": str,
            "csrf_access_token": str,
            "usuario": dict,
        }"""
        res = {
            "ok": True,
            "msg": "Logado com sucesso!",
            "access_token": None,
            "csrf_access_token": None,
            "usuario": None,
        }

        usuario = self.validar_login(email=email, senha=senha)

        if not usuario:
            res["ok"] = False
            res["msg"] = "Email ou Senha inválidos"
            return res

        token = create_access_token(identity=usuario)

        res["access_token"] = token
        res["csrf_access_token"] = get_csrf_token(encoded_token=token)

        res["usuario"] = self.get_user_json(usuario=usuario)

        return res

    def register_user(
        self, nome: str, email: str, senha: str, img_base_url: str
    ):
        """Returns:
        dict: {
            "ok": bool,
            "msg": str,
            "access_token": str,
            "csrf_access_token": str,
            "usuario": dict,
        }"""
        res = {
            "ok": True,
            "msg": "Usuário criado com sucesso!",
            "access_token": None,
            "csrf_access_token": None,
            "usuario": None,
        }

        # validar se usuario ja existe
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            res["ok"] = False
            res["msg"] = "Este email já está em uso"
            return res

        try:
            new_user = self.criar_usuario(
                nome=nome,
                email=email,
                senha=senha,
            )
        except Exception:
            db.session.rollback()
            res["ok"] = False
            res["msg"] = "Erro interno ao criar usuario"
            return res

        token = create_access_token(identity=new_user)

        res["access_token"] = token
        res["csrf_access_token"] = get_csrf_token(encoded_token=token)

        res["usuario"] = self.get_user_json(usuario=new_user)

        return res
