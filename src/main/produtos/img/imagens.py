from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db


class ProdutoImg(db.Model):
    __tablename__ = "ProdutoImg"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    id_estoque: Mapped[int] = mapped_column(
        ForeignKey("ProdutoEstoque.id", ondelete="CASCADE"), nullable=False
    )
    caminho: Mapped[str] = mapped_column(db.String(255), nullable=False)
    ordem: Mapped[int] = mapped_column(
        db.Integer, nullable=False, server_default=text("1")
    )

    estoque = relationship(
        argument="ProdutoEstoque", back_populates="imgs", uselist=False
    )
