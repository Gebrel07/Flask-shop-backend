from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db


class Carrinho(db.Model):
    __tablename__ = "Carrinho"

    id_usuario: Mapped[int] = mapped_column(
        db.Integer,
        ForeignKey("Usuario.id", ondelete="CASCADE"),
        primary_key=True,
    )
    id_estoque: Mapped[int] = mapped_column(
        db.Integer,
        ForeignKey("ProdutoEstoque.id", ondelete="CASCADE"),
        primary_key=True,
    )
    qtd: Mapped[int] = mapped_column(db.Integer, nullable=False)
    data_inclusao: Mapped[int] = mapped_column(db.DateTime, nullable=False)

    estoque = relationship(argument="ProdutoEstoque", uselist=False)
