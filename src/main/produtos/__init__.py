from .caracteristicas import ProdutoCaract
from .estoque import ProdutoEstoque
from .produto import Produto
from .routes import produtos_bp

__all__ = [
    "produtos_bp",
    "Produto",
    "ProdutoCaract",
    "ProdutoEstoque",
]
