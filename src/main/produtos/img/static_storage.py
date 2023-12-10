import os

from flask import url_for

from .imagens import ProdutoImg


class StaticStorage:
    """Handles Images served from the static folder"""

    def __init__(self) -> None:
        self.sub_folder = "prod_imgs"

    def get_img(self, img: ProdutoImg):
        """Builds url for image served from the App's static folder

        Requires request context
        """
        return url_for(
            endpoint="static",
            filename=os.path.join(
                self.sub_folder, os.path.basename(img.caminho)
            ),
            _external=True,
        )  # type: ignore
