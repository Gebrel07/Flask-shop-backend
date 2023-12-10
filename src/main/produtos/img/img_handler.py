from typing import Any, Literal

from flask import current_app

from .imagens import ProdutoImg
from .static_storage import StaticStorage


class ImgHandler:
    def __init__(self, storage_mode: Literal["static"] | None = None) -> None:
        """Handles Images according to where they are being stored.

        Requires application context

        Args:
        storage_mode (Literal['static'] | None): Where the image files are being stored. Defaults \
            to match IMG_STORAGE_MODE config value.
        """
        self.__storage_modes = {"static": StaticStorage}
        self.__default_mode = current_app.config["IMG_STORAGE_MODE"]

        if storage_mode:
            self.storage = self.__storage_modes[storage_mode]()
        else:
            self.storage = self.__storage_modes[self.__default_mode]()

    def get_img_url(self, img: ProdutoImg):
        return self.storage.get_img(img=img)

    def get_prod_img(self, prod: Any):
        """Busca url da primeira imagem de um Produto, se houver.

        Raises:
            TypeError: se prod não for int ou Produto

        Returns:
            str | None: url da img
        """
        if not prod.estoque:
            return None

        for variacao in prod.estoque:
            if variacao.imgs:
                img = variacao.imgs[0]
                return self.get_img_url(img=img)

        return None
