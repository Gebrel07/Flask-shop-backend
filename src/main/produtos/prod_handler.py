import os
from typing import Any

from flask import url_for

from .produto import Produto


class ProdHandler:
    def __init__(self) -> None:
        pass

    def get_destaques(self) -> list[dict[str, Any]] | None:
        query = (
            Produto.query.filter_by(destaque=True).order_by(Produto.nome).all()
        )

        if not query:
            return None

        res = []
        for prod in query:
            aux = {
                "id": prod.id,
                "nome": prod.nome,
                "descricao": prod.descricao,
                "preco": prod.preco,
            }

            img = self.__get_first_img(prod=prod)
            if img:
                aux["img"] = url_for(
                    "static",
                    filename=os.path.basename(img.caminho),
                    _external=True,
                )

            res.append(aux)

        return res

    def __get_first_img(self, prod: Produto):
        if not prod.estoque:
            return None

        for variacao in prod.estoque:
            if variacao.imgs:
                return variacao.imgs[0]

        return None
