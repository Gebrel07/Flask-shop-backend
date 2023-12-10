from flask import Blueprint, request
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies

from src.json_handler import JsonHandler
from src.utils import make_json_resp

from ..usuario.usr import UserHandler

auth_bp = Blueprint(name="auth", import_name=__name__, url_prefix="/auth")


user_handler = UserHandler()
json_handler = JsonHandler()


@auth_bp.route("/login", methods=["POST"])
def login():
    json_data: dict | None = request.get_json(force=True, silent=True)

    validation_res = json_handler.valdidate_keys(
        data=json_data, keys=["email", "senha"]
    )
    if validation_res["ok"] is False:
        return make_json_resp(ok=False, msg=validation_res["erros"])

    assert isinstance(json_data, dict)

    res = user_handler.login_user(
        email=json_data["email"],
        senha=json_data["senha"],
        img_base_url=request.root_url,
    )

    resp = make_json_resp(**res)

    if res["access_token"]:
        set_access_cookies(
            response=resp[0], encoded_access_token=res["access_token"]
        )

    return resp


@auth_bp.route("/register", methods=["POST"])
def register():
    json_data: dict | None = request.get_json(force=True, silent=True)

    validation_res = json_handler.valdidate_keys(
        data=json_data, keys=["nome", "email", "senha"]
    )
    if validation_res["ok"] is False:
        return make_json_resp(ok=False, msg=validation_res["erros"])

    assert isinstance(json_data, dict)

    res = user_handler.register_user(
        nome=json_data["nome"],
        email=json_data["email"],
        senha=json_data["senha"],
        img_base_url=request.root_url,
    )

    resp = make_json_resp(**res)

    if res["access_token"]:
        set_access_cookies(
            response=resp[0], encoded_access_token=res["access_token"]
        )

    return resp


@auth_bp.route("/logout", methods=["POST"])
def logout():
    resp = make_json_resp(ok=True, msg="Deslogado com sucesso!")
    unset_jwt_cookies(response=resp[0])
    return resp


@auth_bp.route("/teste", methods=["POST"])
def teste():
    cookies = request.cookies
    return make_json_resp(ok=True, msg=cookies)
