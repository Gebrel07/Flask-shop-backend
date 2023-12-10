from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.extensions import db


class Endereco(db.Model):
    __tablename__ = "Endereco"

    id: Mapped[int] = mapped_column(
        db.Integer,
        primary_key=True,
    )

    id_usuario: Mapped[int] = mapped_column(
        db.Integer,
        ForeignKey("Usuario.id", ondelete="CASCADE"),
    )

    rua: Mapped[str] = mapped_column(db.String(400), nullable=False)
    numero: Mapped[str] = mapped_column(db.Integer, nullable=False)
    complemento: Mapped[str] = mapped_column(db.String(255), nullable=True)
    bairro: Mapped[str] = mapped_column(db.String(300), nullable=False)
    cidade: Mapped[str] = mapped_column(db.String(255), nullable=False)
    estado: Mapped[str] = mapped_column(db.String(2), nullable=False)
    cep: Mapped[str] = mapped_column(db.Integer, nullable=False)

    data_inclusao: Mapped[int] = mapped_column(db.DateTime, nullable=False)
