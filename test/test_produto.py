from flask import Flask

from src.main.produtos.prod import ProdHandler


def test_get_prods(app: Flask):
    # request context is necessary to build url
    with app.app_context() and app.test_request_context():
        prod = ProdHandler()
        res = prod.get_produtos()

    assert isinstance(res, (dict, None))  # type: ignore

    with app.app_context() and app.test_request_context():
        prod = ProdHandler()
        res = prod.get_produtos(page=9999)

    assert isinstance(res, (dict, None))  # type: ignore


def test_get_destaques(app: Flask):
    with app.app_context() and app.test_request_context():
        prod = ProdHandler()
        res = prod.get_destaques()

    assert isinstance(res, (dict, None))  # type: ignore

    with app.app_context() and app.test_request_context():
        prod = ProdHandler()
        res = prod.get_destaques(page=9999)

    assert isinstance(res, (dict, None))  # type: ignore
