from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db


class Favoritos(db.Model):
    __tablename__ = "Favoritos"

    id_usuario: Mapped[int] = mapped_column(
        db.Integer,
        ForeignKey("Usuario.id", ondelete="CASCADE"),
        primary_key=True,
    )
    id_produto: Mapped[int] = mapped_column(
        db.Integer,
        ForeignKey("Produto.id", ondelete="CASCADE"),
        primary_key=True,
    )
    data_inclusao: Mapped[int] = mapped_column(db.DateTime, nullable=False)

    produto = relationship(argument="Produto", uselist=False)
