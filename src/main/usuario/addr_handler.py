from src.serializer import Serializer

from .enderecos import Endereco
from .usuario import Usuario


class AddrHandler:
    def __init__(self) -> None:
        pass

    def get_enderecos(self, id_usuario: int):
        usuario = Usuario.query.get(id_usuario)

        if not usuario:
            return None

        ser = Serializer(table=Endereco)
        return ser.serialize_many(
            query=usuario.enderecos,
            ignore_attrs=["id_usuario", "data_inclusao"],
        )
