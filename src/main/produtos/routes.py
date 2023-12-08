from urllib.parse import urljoin

from flask import Blueprint, abort, jsonify, request, send_file, url_for

from src.extensions import db
from src.serializer import Serializer
from src.utils import make_json_resp

from .caracteristicas import ProdutoCaract
from .estoque import ProdutoEstoque
from .imagens import ProdutoImg
from .produto import Produto

produtos_bp = Blueprint(
    name="produtos", import_name=__name__, url_prefix="/produtos"
)


@produtos_bp.route("/")
def get_produtos():
    req_args = request.args

    if "nome" in req_args.keys():
        nome = req_args.get(key="nome", type=str)
        query = db.select(Produto).where(Produto.nome.like(f"%{nome}%"))
    else:
        query = db.select(Produto)

    page = req_args.get("page", type=int, default=1)
    pagination = db.paginate(select=query, page=page, per_page=20)

    ser = Serializer(table=Produto)

    res = ser.serialize_pagination(pagination=pagination)

    return jsonify(res)


@produtos_bp.route("/<int:id_prod>")
def get_produto(id_prod: int):
    prod: Produto | None = Produto.query.get(id_prod)

    if not prod:
        return make_json_resp(
            ok=False, msg="Produto não encontrado", status=404
        )

    ser = Serializer(table=Produto)
    prod_json = ser.serialize(obj=prod)

    if prod.caracts:
        prod_json["caracteristicas"] = __get_caracts(prod=prod)

    if prod.estoque:
        prod_json["estoque"] = __get_estoque(prod=prod)

    res = make_json_resp(ok=True, prod=prod_json)

    return res


@produtos_bp.route("/imgs/<int:id_img>")
def get_img_produto(id_img: int):
    img: ProdutoImg | None = ProdutoImg.query.get(id_img)

    if not img:
        return abort(404)

    return send_file(path_or_file=img.caminho)


def __get_caracts(prod: Produto):
    ser = Serializer(table=ProdutoCaract)
    res = ser.serialize_many(
        query=prod.caracts, ignore_attrs=["id", "id_produto"]
    )
    return res


def __get_estoque(prod: Produto):
    res = []
    for stq in prod.estoque:
        aux = {
            "id": stq.id,
            "tamanho": stq.tamanho,
            "cor": stq.cor,
            "qtd": stq.qtd,
        }

        if stq.imgs:
            aux["imgs"] = __get_imgs(estoque=stq)

        res.append(aux)

    return res


def __get_imgs(estoque: ProdutoEstoque):
    res = []
    for img in estoque.imgs:
        url = urljoin(
            base=request.root_url,
            url=url_for(endpoint="produtos.get_img_produto", id_img=img.id),
        )
        res.append(url)
    return res
