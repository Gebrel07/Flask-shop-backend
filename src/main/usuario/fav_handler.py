from datetime import datetime
from typing import Any
from urllib.parse import urljoin

from flask import url_for
from sqlalchemy.exc import IntegrityError

from src.extensions import db

from ..produtos import Produto
from .favoritos import Favoritos
from .usuario import Usuario


class FavHandler:
    def __init__(self) -> None:
        pass

    def get_favoritos(
        self, id_usuario: int, img_base_url: str
    ) -> list[dict[str, Any]] | None:
        usuario = Usuario.query.get(id_usuario)

        if not usuario:
            return None

        fav_items = []
        for item in usuario.favoritos:
            aux = {
                "id_prod": item.produto.id,
                "nome": item.produto.nome,
                "preco": item.produto.preco,
            }

            if item.produto.estoque:
                # get first img url
                img = item.produto.estoque[0].imgs[0]
                url = urljoin(
                    base=img_base_url,
                    url=url_for(
                        endpoint="produtos.get_img_produto", id_img=img.id
                    ),
                )
                aux["img"] = url

            fav_items.append(aux)

        return fav_items

    def __get_fav_ids(self, id_usuario: int) -> list[int] | None:
        usuario = Usuario.query.get(id_usuario)

        if not usuario:
            return None

        ids = []
        for fav in usuario.favoritos:
            ids.append(fav.id_produto)

        return ids

    def adicionar_item(
        self, id_usuario: int, id_produto: int
    ) -> dict[str, Any]:
        """Adiciona Produto à lista de favoritos do Usuário

        Returns:
            dict: {ok: bool, msg: str, favoritos: list[int]}
        """
        res = {
            "ok": True,
            "msg": "Adicionado com sucesso!",
            "favoritos": self.__get_fav_ids(id_usuario=id_usuario),
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
            res["favoritos"] = self.__get_fav_ids(id_usuario=id_usuario)
            return res
        except IntegrityError:
            return res
        except Exception:
            db.session.rollback()
            res["ok"] = False
            res["msg"] = "Erro interno ao adicionar aos favoritos"
            return res

    def remover_item(self, id_usuario: int, id_produto: int):
        """Remove Produto da lista de Favoritos do Usuário

        Returns:
            dict: {ok: bool, msg: str, favoritos: list[int]}"""
        res = {
            "ok": True,
            "msg": "Removido com sucesso!",
            "favoritos": self.__get_fav_ids(id_usuario=id_usuario),
        }

        fav = Favoritos.query.get((id_usuario, id_produto))

        if not fav:
            return res

        try:
            db.session.delete(fav)
            db.session.commit()
            res["favoritos"] = self.__get_fav_ids(id_usuario=id_usuario)
            return res
        except Exception:
            db.session.rollback()
            res["ok"] = False
            res["msg"] = "Erro interno ao remover dos favoritos"
            return res
