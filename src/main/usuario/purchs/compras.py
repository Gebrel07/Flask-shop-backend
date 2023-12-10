from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from src.extensions import db


class Compra(db.Model):
    __tablename__ = "Compra"

    id: Mapped[int] = mapped_column(
        db.Integer,
        primary_key=True,
    )

    id_usuario: Mapped[int] = mapped_column(
        db.Integer,
        ForeignKey("Usuario.id", ondelete="CASCADE"),
    )
    id_estoque: Mapped[int] = mapped_column(
        db.Integer,
        ForeignKey("Estoque.id", ondelete="CASCADE"),
    )

    qtd: Mapped[str] = mapped_column(db.Integer, nullable=False)

    pago: Mapped[bool] = mapped_column(
        db.Boolean, nullable=False, server_default=text("0")
    )
    enviado: Mapped[bool] = mapped_column(
        db.Boolean, nullable=False, server_default=text("0")
    )
    recebido: Mapped[bool] = mapped_column(
        db.Boolean, nullable=False, server_default=text("0")
    )

    data_inclusao: Mapped[int] = mapped_column(db.DateTime, nullable=False)
    data_pgto: Mapped[int] = mapped_column(db.DateTime)
    data_envio: Mapped[int] = mapped_column(db.DateTime)
    data_recebido: Mapped[int] = mapped_column(db.DateTime)
