from flask import Blueprint, request
from flask_jwt_extended import get_current_user, jwt_required

from src.utils import make_json_resp, validate_json_data, validate_user_id

from .addr import AddrHandler
from .cart import CartHandler
from .fav import FavHandler
from .usr import UserHandler, Usuario

usuario_bp = Blueprint(
    name="usuario", import_name=__name__, url_prefix="/usuarios"
)


@usuario_bp.route("/", methods=["POST"])
@jwt_required()
def get_usuario():
    usuario = get_current_user()
    handler = UserHandler()
    user_json = handler.get_user_json(usuario=usuario)
    return make_json_resp(ok=True, usuario=user_json)


@usuario_bp.route("/<int:id_usuario>/favoritos/", methods=["GET"])
@jwt_required()
def get_favs(id_usuario: int):
    usuario = Usuario.query.get(id_usuario)

    if not usuario:
        return make_json_resp(
            ok=False,
            msg=f"Usuário de ID: {id_usuario} não encontrado",
            status=404,
        )

    validate_user = validate_user_id(user_id=id_usuario)
    if not validate_user["ok"]:
        return validate_user["resp"]

    fav = FavHandler()
    res = fav.get_user_favs(usuario=usuario)

    return make_json_resp(ok=True, res=res)


@usuario_bp.route("/<int:id_usuario>/favoritos/", methods=["POST"])
@jwt_required()
def add_fav(id_usuario: int):
    usuario = Usuario.query.get(id_usuario)

    if not usuario:
        return make_json_resp(
            ok=False,
            msg=f"Usuário de ID: {id_usuario} não encontrado",
            status=404,
        )

    validate_user = validate_user_id(user_id=id_usuario)
    if not validate_user["ok"]:
        return validate_user["resp"]

    json_data = request.get_json(force=True, silent=True)
    validate_json = validate_json_data(json_data=json_data, keys=["id"])
    if not validate_json["ok"]:
        return validate_json["resp"]

    assert json_data

    fav = FavHandler()
    res = fav.add_fav(id_usuario=usuario.id, id_produto=json_data["id"])

    return make_json_resp(ok=res["ok"], msg=res["msg"])


@usuario_bp.route(
    "/<int:id_usuario>/favoritos/<int:id_produto>/", methods=["DELETE"]
)
@jwt_required()
def remove_fav(id_usuario: int, id_produto: int):
    usuario = Usuario.query.get(id_usuario)

    if not usuario:
        return make_json_resp(
            ok=False,
            msg=f"Usuário de ID: {id_usuario} não encontrado",
            status=404,
        )

    validate_user = validate_user_id(user_id=id_usuario)
    if not validate_user["ok"]:
        return validate_user["resp"]

    fav = FavHandler()
    res = fav.remove_fav(id_usuario=usuario.id, id_produto=id_produto)

    return make_json_resp(ok=res["ok"], msg=res["msg"])


@usuario_bp.route("/<int:id_usuario>/carrinho/", methods=["GET"])
@jwt_required()
def get_carrinho(id_usuario: int):
    usuario = Usuario.query.get(id_usuario)

    if not usuario:
        return make_json_resp(
            ok=False,
            msg=f"Usuário de ID: {id_usuario} não encontrado",
            status=404,
        )

    validate_user = validate_user_id(user_id=id_usuario)
    if not validate_user["ok"]:
        return validate_user["resp"]

    cart = CartHandler()
    res = cart.get_user_cart(usuario=usuario)

    return make_json_resp(ok=True, res=res)


@usuario_bp.route("/<int:id_usuario>/carrinho/", methods=["POST"])
@jwt_required()
def add_to_cart(id_usuario: int):
    usuario = Usuario.query.get(id_usuario)

    if not usuario:
        return make_json_resp(
            ok=False,
            msg=f"Usuário de ID: {id_usuario} não encontrado",
            status=404,
        )

    validate_user = validate_user_id(user_id=id_usuario)
    if not validate_user["ok"]:
        return validate_user["resp"]

    json_data = request.get_json(force=True, silent=True)
    validate_json = validate_json_data(json_data=json_data, keys=["id", "qtd"])
    if not validate_json["ok"]:
        return validate_json["resp"]

    assert json_data

    cart = CartHandler()
    res = cart.add_item(
        id_usuario=usuario.id, id_estoque=json_data["id"], qtd=json_data["qtd"]
    )

    return make_json_resp(ok=res["ok"], msg=res["msg"])


@usuario_bp.route(
    "/<int:id_usuario>/carrinho/<int:id_estoque>/", methods=["DELETE"]
)
@jwt_required()
def remove_from_cart(id_usuario: int, id_estoque: int):
    usuario = Usuario.query.get(id_usuario)

    if not usuario:
        return make_json_resp(
            ok=False,
            msg=f"Usuário de ID: {id_usuario} não encontrado",
            status=404,
        )

    validate_user = validate_user_id(user_id=id_usuario)
    if not validate_user["ok"]:
        return validate_user["resp"]

    cart = CartHandler()
    res = cart.remove_item(id_usuario=usuario.id, id_estoque=id_estoque)

    return make_json_resp(ok=res["ok"], msg=res["msg"])


@usuario_bp.route("/<int:id_usuario>/enderecos/", methods=["GET"])
@jwt_required()
def get_enderecos(id_usuario: int):
    usuario = Usuario.query.get(id_usuario)

    if not usuario:
        return make_json_resp(
            ok=False,
            msg=f"Usuário de ID: {id_usuario} não encontrado",
            status=404,
        )

    validate_user = validate_user_id(user_id=id_usuario)
    if not validate_user["ok"]:
        return validate_user["resp"]

    addr = AddrHandler()
    res = addr.get_user_addrs(usuario=usuario)

    return make_json_resp(ok=True, res=res)
