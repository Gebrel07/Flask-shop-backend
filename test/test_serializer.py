from src.serializer import Serializer
from src.main.produtos import Produto


def test_serialize_one():
    s = Serializer(table=Produto)

    prod = Produto(
        id=1,
        nome="prod 1",
        preco=99.99,
    )  # type: ignore

    res = s.serialize(obj=prod)

    assert res

    for k in ("id", "nome", "preco"):
        assert res.get(k) == getattr(prod, k)


def test_serialize_many():
    s = Serializer(table=Produto)

    query = []
    for i in range(1, 5):
        aux = Produto(
            id=i,
            nome=f"prod {i}",
            preco=99.99,
        )  # type: ignore
        query.append(aux)

    res = s.serialize_many(query=query)

    assert len(query) == len(res)

    for idx, prod in enumerate(query):
        for k in ("id", "nome", "preco"):
            assert res[idx].get(k) == getattr(prod, k)
