from flask import Blueprint, request

from src.utils import make_json_resp

from .prod import ProdHandler

produtos_bp = Blueprint(
    name="produtos", import_name=__name__, url_prefix="/produtos"
)


@produtos_bp.route("/")
def get_produtos():
    prod_handler = ProdHandler()
    res = prod_handler.get_produtos(
        nome=request.args.get("nome", default=None),
        page=request.args.get("page", type=int, default=1),
    )
    return make_json_resp(ok=True, res=res)


@produtos_bp.route("/<int:id_prod>")
def get_produto(id_prod: int):
    prod_handler = ProdHandler()
    res = prod_handler.get_prod_json(id_prod)
    if not res:
        return make_json_resp(
            ok=False, msg="Produto não encontrado", status=404
        )
    return make_json_resp(ok=True, res=res)


@produtos_bp.route("/destaques")
def get_destaques():
    prod_handler = ProdHandler()
    res = prod_handler.get_destaques(
        page=request.args.get("page", type=int, default=1),
    )
    return make_json_resp(ok=True, res=res)
