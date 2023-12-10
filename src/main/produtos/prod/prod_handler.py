from typing import Any

from src.extensions import db
from src.utils import get_pagination_json

from ..caract import CharactHandler
from ..estoque import EstqHandler
from ..img import ImgHandler
from .produto import Produto


class ProdHandler:
    def __init__(
        self,
        res_per_page: int = 20,
    ) -> None:
        self.per_page = res_per_page
        self.img_handler = ImgHandler()
        self.caract_handler = CharactHandler()
        self.estq_handler = EstqHandler()

    def get_prod_json(self, prod: int | Produto) -> dict[str, Any] | None:
        if isinstance(prod, int):
            prod_obj = Produto.query.get(prod)
        elif isinstance(prod, Produto):
            prod_obj = prod
        else:
            raise TypeError(f"prod must be of type int or {Produto.__name__}")

        if not prod_obj:
            return None

        assert isinstance(prod_obj, Produto)

        res = {
            "id": prod_obj.id,
            "nome": prod_obj.nome,
            "descricao": prod_obj.descricao,
            "preco": prod_obj.preco,
            "destaque": prod_obj.destaque,
            "img": self.img_handler.get_prod_img(prod=prod_obj),
            "caracteristicas": self.caract_handler.get_characts(prod=prod_obj),
            "estoque": self.estq_handler.get_estq(prod=prod_obj),
        }
        return res

    def get_produtos(self, nome: str | None = None, page: int = 1):
        if nome:
            query = db.select(Produto).where(Produto.nome.like(f"%{nome}%"))
        else:
            query = db.select(Produto)

        pagination = db.paginate(
            select=query, page=page, per_page=self.per_page, error_out=False
        )

        prods = []
        for prod in pagination.items:
            prods.append(self.get_prod_json(prod=prod))

        res = get_pagination_json(pagination=pagination, data=prods)

        return res

    def get_destaques(self, page: int = 1):
        query = Produto.query.filter_by(destaque=True).paginate(
            page=page, per_page=self.per_page, error_out=False
        )

        prods = []
        for prod in query.items:
            prods.append(self.get_prod_json(prod=prod))

        res = get_pagination_json(pagination=query, data=prods)

        return res
