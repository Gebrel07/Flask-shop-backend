from datetime import datetime
from typing import Any

from flask import url_for

from src.extensions import db

from ..produtos import ProdutoEstoque
from .carrinho import Carrinho
from .usuario import Usuario


class CartHandler:
    def __init__(self) -> None:
        pass

    def get_carrinho(self, id_usuario: int) -> list[dict[str, Any]] | None:
        usuario = Usuario.query.get(id_usuario)

        if not usuario:
            return None

        cart_items = []
        for item in usuario.carrinho:
            aux = {
                "id_prod": item.estoque.produto.id,
                "nome": item.estoque.produto.nome,
                "preco": item.estoque.produto.preco,
                "id_estoque": item.id_estoque,
                "cor": item.estoque.cor,
                "tamanho": item.estoque.tamanho,
                "qtd": item.qtd,
            }

            if item.estoque.imgs:
                # get first img url
                img = item.estoque.imgs[0]
                url = url_for(
                    endpoint="produtos.get_img_produto",
                    _external=True,
                    id_img=img.id,
                )
                aux["img"] = url

            cart_items.append(aux)

        return cart_items

    def __get_cart_ids(self, id_usuario: int) -> list[int] | None:
        usuario = Usuario.query.get(id_usuario)

        if not usuario:
            return None

        ids = []
        for item in usuario.carrinho:
            ids.append(item.id_estoque)

        return ids

    def adicionar_item(
        self, id_usuario: int, id_estoque: int, qtd: int
    ) -> dict[str, Any]:
        """Adiciona item do Estoque ao Carrinho de compras

        Returns:
            dict: {ok: bool, msg: str, carrinho: list[int]}
        """
        res = {
            "ok": True,
            "msg": "Adicionado com sucesso!",
            "carrinho": self.__get_cart_ids(id_usuario=id_usuario),
        }

        estoque = ProdutoEstoque.query.get(id_estoque)

        # validar estoque
        if not estoque:
            res["ok"] = False
            res["msg"] = f"Estoque de ID: {id_estoque} não encontrado"
            return res

        if estoque.qtd <= 0:
            res["ok"] = False
            res["msg"] = "Produto indisponível no Estoque"
            return res

        # validar qtd
        if qtd < 1 or qtd > estoque.qtd:
            res["ok"] = False
            res["msg"] = f"Qtd inválida. Min: 1 | Max: {estoque.qtd}"
            return res

        item_carrinho = Carrinho.query.get((id_usuario, id_estoque))

        if item_carrinho:
            # modificar item existente
            try:
                item_carrinho.qtd = qtd
                db.session.commit()
                res["carrinho"] = self.__get_cart_ids(id_usuario=id_usuario)
                return res
            except Exception:
                db.session.rollback()
                res["ok"] = False
                res["msg"] = "Erro interno ao adicionar ao carrinho"
                return res
        else:
            # adicionar item novo
            try:
                new_cart_item = Carrinho(
                    id_usuario=id_usuario,
                    id_estoque=id_estoque,
                    qtd=qtd,
                    data_inclusao=datetime.now(),
                )  # type: ignore
                db.session.add(new_cart_item)
                db.session.commit()
                res["carrinho"] = self.__get_cart_ids(id_usuario=id_usuario)
                return res
            except Exception:
                db.session.rollback()
                res["ok"] = False
                res["msg"] = "Erro interno ao adicionar ao carrinho"
                return res

    def remover_item(self, id_usuario: int, id_estoque: int) -> dict[str, Any]:
        """Remove item do Carrinho de compras

        Returns:
            dict: {ok: bool, msg: str, carrinho: list[int]}
        """
        res = {
            "ok": True,
            "msg": "Removido com sucesso!",
            "carrinho": self.__get_cart_ids(id_usuario=id_usuario),
        }

        item = Carrinho.query.get((id_usuario, id_estoque))

        if not item:
            return res

        try:
            db.session.delete(item)
            db.session.commit()
            res["carrinho"] = self.__get_cart_ids(id_usuario=id_usuario)
            return res
        except Exception:
            db.session.rollback()
            res["ok"] = False
            res["msg"] = "Erro interno ao remover do carrinho"
            return res
