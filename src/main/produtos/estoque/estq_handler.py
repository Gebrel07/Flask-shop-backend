from typing import Any

from ..img import ImgHandler
from .estoque import ProdutoEstoque


class EstqHandler:
    def __init__(self) -> None:
        self.img_handler = ImgHandler()

    def get_estq_json(self, estq: ProdutoEstoque) -> dict[str, Any]:
        res = {
            "id": estq.id,
            "variacao": estq.variacao,
            "tamanho": estq.tamanho,
            "cor": estq.cor,
            "qtd": estq.qtd,
        }
        if estq.imgs:
            res["imgs"] = [
                self.img_handler.get_img_url(img=img) for img in estq.imgs
            ]
        return res

    def get_estq(self, prod: Any) -> list[dict[str, Any]]:
        res = []
        for estq in prod.estoque:
            res.append(self.get_estq_json(estq=estq))
        return res
