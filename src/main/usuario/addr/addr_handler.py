from typing import Any

from .enderecos import Endereco


class AddrHandler:
    def __init__(self) -> None:
        pass

    def get_addr_json(self, addr: Endereco):
        res = {
            "id": addr.id,
            "rua": addr.rua,
            "numero": addr.numero,
            "complemento": addr.complemento,
            "bairro": addr.bairro,
            "cidade": addr.cidade,
            "estado": addr.estado,
            "cep": addr.cep,
        }
        return res

    def get_user_addrs(self, usuario: Any):
        res = []
        for addr in usuario.enderecos:
            res.append(self.get_addr_json(addr=addr))
        return res
