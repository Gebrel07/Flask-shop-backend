from .custom_client import TestClient


def test_get_cart(client: TestClient):
    client.login_client(id_usuario=1)

    key, val = client.get_x_csrf_header() or (0, 0)

    resp = client.get("usuarios/1/carrinho/", headers={key: val})

    assert resp is not None
    assert resp.status_code == 200
    assert isinstance(resp.json["res"], list)  # type: ignore


def test_add_to_cart(client: TestClient):
    client.login_client(id_usuario=1)

    key, val = client.get_x_csrf_header() or (0, 0)

    resp = client.post(
        "usuarios/1/carrinho/", json={"id": 1, "qtd": 1}, headers={key: val}
    )

    assert resp is not None
    assert resp.status_code == 200


def test_remove_from_cart(client: TestClient):
    client.login_client(id_usuario=1)

    key, val = client.get_x_csrf_header() or (0, 0)

    resp = client.delete("usuarios/1/carrinho/1/", headers={key: val})

    assert resp is not None
    assert resp.status_code == 200


def test_get_favs(client: TestClient):
    client.login_client(id_usuario=1)

    key, val = client.get_x_csrf_header() or (0, 0)

    resp = client.get("usuarios/1/favoritos/", headers={key: val})

    assert resp is not None
    assert resp.status_code == 200
    assert isinstance(resp.json["res"], list)  # type: ignore


def test_add_to_fav(client: TestClient):
    client.login_client(id_usuario=1)

    key, val = client.get_x_csrf_header() or (0, 0)

    resp = client.post(
        "usuarios/1/favoritos/", json={"id": 1, "qtd": 1}, headers={key: val}
    )

    assert resp is not None
    assert resp.status_code == 200


def test_remove_from_fav(client: TestClient):
    client.login_client(id_usuario=1)

    key, val = client.get_x_csrf_header() or (0, 0)

    resp = client.delete("usuarios/1/favoritos/1/", headers={key: val})

    assert resp is not None
    assert resp.status_code == 200


def test_get_enderecos(client: TestClient):
    client.login_client(id_usuario=1)

    key, val = client.get_x_csrf_header() or (0, 0)

    resp = client.get("usuarios/1/enderecos/", headers={key: val})

    assert resp is not None
    assert resp.status_code == 200
    assert isinstance(resp.json["res"], list)  # type: ignore
