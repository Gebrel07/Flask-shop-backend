from .caract import ProdutoCaract
from .estoque import ProdutoEstoque
from .img.imagens import ProdutoImg
from .prod import Produto
from .routes import produtos_bp

__all__ = [
    "produtos_bp",
    "Produto",
    "ProdutoCaract",
    "ProdutoEstoque",
    "ProdutoImg",
]
