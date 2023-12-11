import os

from dotenv import load_dotenv
from flask import Flask
from typing import Any


class Config:
    def __init__(self) -> None:
        load_dotenv(dotenv_path=".flaskenv")

        self.SECRET_KEY = self.get_env_var(key="SECRET_KEY")

        self.SQLALCHEMY_DATABASE_URI = self.get_env_var(
            key="SQLALCHEMY_DATABASE_URI"
        )
        self.SQLALCHEMY_ECHO = False
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

        self.CORS_SUPPORTS_CREDENTIALS = True
        self.CORS_ORIGINS = self.get_env_var(key="CORS_ORIGINS")

        self.JWT_SECRET_KEY = self.get_env_var(key="JWT_SECRET_KEY")
        self.JWT_TOKEN_LOCATION = ["cookies", "headers", "json"]
        self.JWT_ACCESS_TOKEN_EXPIRES = self.get_env_var(
            key="JWT_ACCESS_TOKEN_EXPIRES"
        )
        self.JWT_COOKIE_SAMESITE = self.get_env_var(key="JWT_COOKIE_SAMESITE")
        self.JWT_COOKIE_SECURE = self.get_env_var(key="JWT_COOKIE_SECURE")
        self.JWT_COOKIE_CSRF_PROTECT = True
        self.JWT_CSRF_IN_COOKIES = True

        self.PROD_IMGS = self.get_env_var(key="PROD_IMGS")
        self.IMG_STORAGE_MODE = self.get_env_var(key="IMG_STORAGE_MODE")

    def get_env_var(self, key: str) -> Any:
        val = os.getenv(key=key)

        if val is None:
            raise TypeError(f"Variável {key} não encontrada no ambiente")

        if val == "True":
            return True

        if val == "False":
            return False

        if "," in val:
            return val.replace(" ", "").split(sep=",")

        if val.isnumeric():
            return int(val)

        return val

    def assert_app_configs(self, app: Flask):
        for key, val in self.__dict__.items():
            app_conf = app.config.get(key)

            if app_conf != val:
                raise ValueError(f"Configuração incorreta em {key}")
