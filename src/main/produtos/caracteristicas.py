from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.extensions import db


class ProdutoCaract(db.Model):
    __tablename__ = "ProdutoCaract"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    id_produto: Mapped[int] = mapped_column(
        ForeignKey("Produto.id", ondelete="CASCADE"), nullable=False
    )
    nome: Mapped[str] = mapped_column(db.String(100), nullable=False)
    descr: Mapped[str] = mapped_column(db.String(255), nullable=False)
