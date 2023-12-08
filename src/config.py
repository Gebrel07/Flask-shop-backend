import json
from typing import Any


class Config:
    def __init__(self, json_path: str) -> None:
        self.__REQUIRED_KEYS = [
            "SECRET_KEY",
            "SESSION_COOKIE_HTTPONLY",
            "SESSION_COOKIE_SECURE",
            "SESSION_COOKIE_SAMESITE",
            "SQLALCHEMY_DATABASE_URI",
            "JWT_SECRET_KEY"
        ]

        self.__json_path = json_path

        self.load_json_config()

        return None

    def load_json_config(self):
        with open(self.__json_path) as f:
            new_vals = json.load(f)

            self.__validate_json_vals(vals=new_vals)

            self.__load_json_vals(vals=new_vals)
        return None

    def __validate_json_vals(self, vals: dict[str, Any]):
        for key in self.__REQUIRED_KEYS:
            if key not in vals.keys():
                raise KeyError(f"Erro de Configuração: {key} é obrigatório")

            if vals.get(key) in ("", None):
                raise ValueError(
                    f"Erro de Configuração: {key} não pode ser nulo"
                )

        return None

    def __load_json_vals(self, vals: dict[str, Any]):
        for key, val in vals.items():
            setattr(self, key, val)
        return None
