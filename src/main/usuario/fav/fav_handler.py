from datetime import datetime
from typing import Any

from sqlalchemy.exc import IntegrityError

from src.extensions import db
from src.main.produtos import Produto
from src.main.produtos.img import ImgHandler

from .favoritos import Favoritos


class FavHandler:
    def __init__(self) -> None:
        self.img_handler = ImgHandler()

    def get_fav_json(self, fav: Favoritos) -> dict[str, Any]:
        res = {
            "id": fav.id_produto,
            "nome": fav.produto.nome,
            "preco": fav.produto.preco,
            "img": self.img_handler.get_prod_img(prod=fav.produto),
        }
        return res

    def get_user_favs(self, usuario: Any):
        if not usuario.favoritos:
            return None

        favs = []
        for fav in usuario.favoritos:
            favs.append(self.get_fav_json(fav=fav))

        return favs

    def add_fav(self, id_usuario: int, id_produto: int) -> dict[str, Any]:
        """Adiciona Produto à lista de favoritos do Usuário

        Returns:
            dict: {ok: bool, msg: str}
        """
        res = {
            "ok": True,
            "msg": "Adicionado com sucesso!",
        }

        prod = Produto.query.get(id_produto)

        if not prod:
            res["ok"] = False
            res["msg"] = f"Produto de ID: {id_produto} não encontrado"
            return res

        new_fav = Favoritos(
            id_usuario=id_usuario,
            id_produto=id_produto,
            data_inclusao=datetime.now(),
        )  # type: ignore

        try:
            db.session.add(new_fav)
            db.session.commit()
            return res
        except IntegrityError:
            return res
        except Exception:
            db.session.rollback()
            res["ok"] = False
            res["msg"] = "Erro interno ao adicionar aos favoritos"
            return res

    def remove_fav(self, id_usuario: int, id_produto: int):
        """Remove Produto da lista de Favoritos do Usuário

        Returns:
            dict: {ok: bool, msg: str}"""
        res = {
            "ok": True,
            "msg": "Removido com sucesso!",
        }

        fav = Favoritos.query.get((id_usuario, id_produto))

        if not fav:
            return res

        try:
            db.session.delete(fav)
            db.session.commit()
            return res
        except Exception:
            db.session.rollback()
            res["ok"] = False
            res["msg"] = "Erro interno ao remover dos favoritos"
            return res
