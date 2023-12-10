from typing import List

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db

from ..img import ProdutoImg


class ProdutoEstoque(db.Model):
    __tablename__ = "ProdutoEstoque"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    id_produto: Mapped[int] = mapped_column(
        ForeignKey("Produto.id", ondelete="CASCADE"), nullable=False
    )
    variacao: Mapped[int] = mapped_column(
        db.Integer, nullable=False, server_default=text("1")
    )
    tamanho: Mapped[str] = mapped_column(db.String(255), nullable=False)
    cor: Mapped[str] = mapped_column(db.String(255), nullable=False)
    qtd: Mapped[int] = mapped_column(
        db.Integer, nullable=False, server_default=text("0")
    )

    imgs: Mapped[List["ProdutoImg"]] = relationship(
        argument="ProdutoImg",
        order_by=ProdutoImg.ordem,
        cascade="all, delete",
        passive_deletes=True,
        back_populates="estoque",
    )

    produto = relationship(
        argument="Produto", back_populates="estoque", uselist=False
    )
