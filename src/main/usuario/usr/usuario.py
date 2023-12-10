from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db

from ..addr import Endereco
from ..cart import Carrinho
from ..fav import Favoritos


class Usuario(db.Model):
    __tablename__ = "Usuario"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(db.String(300), nullable=False)
    email: Mapped[str] = mapped_column(
        db.String(300), nullable=False, unique=True
    )
    senha: Mapped[str] = mapped_column(db.String(300), nullable=False)

    favoritos: Mapped[List[Favoritos]] = relationship(
        argument="Favoritos",
        cascade="all, delete",
        passive_deletes=True,
        order_by=Favoritos.data_inclusao,
    )
    carrinho: Mapped[List[Carrinho]] = relationship(
        argument="Carrinho",
        cascade="all, delete",
        passive_deletes=True,
        order_by=Carrinho.data_inclusao,
    )

    enderecos: Mapped[List[Endereco]] = relationship(
        argument="Endereco",
        cascade="all, delete",
        passive_deletes=True,
        order_by=Endereco.rua,
    )
