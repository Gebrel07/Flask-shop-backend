from typing import List

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db

from .caracteristicas import ProdutoCaract
from .estoque import ProdutoEstoque


class Produto(db.Model):
    __tablename__ = "Produto"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(db.String(400), nullable=False)
    descricao: Mapped[str] = mapped_column(db.String(500), nullable=True)
    preco: Mapped[float] = mapped_column(
        db.Float(2), nullable=False, server_default=text("0")
    )
    destaque: Mapped[bool] = mapped_column(
        db.Boolean, nullable=False, server_default=text("0")
    )

    # relationships
    caracts: Mapped[List["ProdutoCaract"]] = relationship(
        argument="ProdutoCaract",
        cascade="all, delete",
        passive_deletes=True,
        order_by=ProdutoCaract.nome,
    )

    estoque: Mapped[List["ProdutoEstoque"]] = relationship(
        argument="ProdutoEstoque",
        back_populates="produto",
        cascade="all, delete",
        passive_deletes=True,
        order_by=ProdutoEstoque.variacao,
    )
