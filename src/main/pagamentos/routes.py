from flask import Blueprint

from src.utils import make_json_resp

from .payment_handler import PaymentHandler

pagamentos_bp = Blueprint(
    name="pagamentos", import_name=__name__, url_prefix="/pagamentos"
)


@pagamentos_bp.route("/meios")
def get_meios_pgto():
    payment = PaymentHandler()
    res = payment.get_formas_pgto()
    return make_json_resp(ok=True, pagamentos=res)
