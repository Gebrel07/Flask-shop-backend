from typing import Any

from .caracteristicas import ProdutoCaract


class CharactHandler:
    def __init__(self) -> None:
        pass

    def get_charact_json(self, charact: ProdutoCaract) -> dict[str, Any]:
        res = {
            "id": charact.id,
            "nome": charact.nome,
            "descr": charact.descr,
        }
        return res

    def get_characts(self, prod: Any) -> list[dict[str, Any]]:
        res = []
        for charact in prod.caracts:
            res.append(self.get_charact_json(charact=charact))
        return res
