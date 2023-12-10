from datetime import datetime
from typing import Any

from src.extensions import db
from src.main.produtos import ProdutoEstoque
from src.main.produtos.img import ImgHandler

from ..usr import Usuario
from .carrinho import Carrinho


class CartHandler:
    def __init__(self) -> None:
        self.img_handler = ImgHandler()

    def get_cart_json(self, cart: Carrinho) -> dict[str, Any]:
        res = {
            "id": cart.id_estoque,
            "nome": cart.estoque.produto.nome,
            "preco": cart.estoque.produto.preco,
            "img": self.img_handler.get_prod_img(prod=cart.estoque.produto),
            "cor": cart.estoque.cor,
            "tamanho": cart.estoque.tamanho,
            "qtd": cart.qtd,
        }
        return res

    def get_user_cart(self, usuario: Usuario) -> list[dict[str, Any]] | None:
        if not usuario.carrinho:
            return None

        cart = []
        for item in usuario.carrinho:
            cart.append(self.get_cart_json(cart=item))

        return cart

    def add_item(
        self, id_usuario: int, id_estoque: int, qtd: int
    ) -> dict[str, Any]:
        """Adiciona item do Estoque ao Carrinho de compras

        Returns:
            dict: {ok: bool, msg: str}
        """
        res = {
            "ok": True,
            "msg": "Adicionado com sucesso!",
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
                return res
            except Exception:
                db.session.rollback()
                res["ok"] = False
                res["msg"] = "Erro interno ao adicionar ao carrinho"
                return res

    def remove_item(self, id_usuario: int, id_estoque: int) -> dict[str, Any]:
        """Remove item do Carrinho de compras

        Returns:
            dict: {ok: bool, msg: str}
        """
        res = {
            "ok": True,
            "msg": "Removido com sucesso!",
        }

        item = Carrinho.query.get((id_usuario, id_estoque))

        if not item:
            return res

        try:
            db.session.delete(item)
            db.session.commit()
            return res
        except Exception:
            db.session.rollback()
            res["ok"] = False
            res["msg"] = "Erro interno ao remover do carrinho"
            return res
