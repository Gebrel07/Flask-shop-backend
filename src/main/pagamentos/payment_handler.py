import copy

from flask import url_for


class PaymentHandler:
    def __init__(self) -> None:
        self.FORMAS_PGTO = [
            {
                "id": 1,
                "nome": "Cartão de Crédito",
                "img": "credit_card.svg",
            },
            {
                "id": 2,
                "nome": "Pix",
                "img": "pix.svg",
            },
            {
                "id": 3,
                "nome": "Boleto",
                "img": "barcode.svg",
            },
        ]

    def get_formas_pgto(self):
        res = copy.deepcopy(self.FORMAS_PGTO)
        for pag in res:
            pag["img"] = url_for("static", filename=pag["img"], _external=True)
        return res
