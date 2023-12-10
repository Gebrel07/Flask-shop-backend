from flask import Flask

from src.main.produtos.img import ProdutoImg, StaticStorage


def test_get_static_img(app: Flask):
    with app.app_context() and app.test_request_context():
        store = StaticStorage()
        img = ProdutoImg.query.first()

        if not img:
            return None

        res = store.get_img(img=img)

    assert isinstance(res, (str, None))  # type: ignore
    if isinstance(img, str):
        assert "/static/" in img
