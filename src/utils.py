from typing import Any, Iterable

import pandas as pd
from flask import jsonify
from flask_jwt_extended import get_current_user
from flask_sqlalchemy.pagination import Pagination
from flask_sqlalchemy.query import Query

from src.extensions import db


def gen_pagination_resp(query: Query, pagination: Pagination):
    res = {
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "page": pagination.page,
        "pages": pagination.pages,
    }

    df = pd.read_sql(sql=query.statement, con=db.session.get_bind()).to_dict(
        orient="records"
    )

    res["dados"] = df

    return res


def make_json_resp(
    ok: bool, msg: Any | None = None, status: int = 200, **kwargs
):
    """Response JSON padrão"""
    res = {"ok": ok, "msg": msg}

    if kwargs:
        res.update(kwargs)

    return jsonify(res), status


def get_pagination_json(
    pagination: Pagination, data: list[dict[str, Any]]
) -> dict[str, Any]:
    res = {"data": data}

    attrs = (
        "has_next",
        "has_prev",
        "page",
        "pages",
        "per_page",
    )

    for attr in attrs:
        res[attr] = getattr(pagination, attr)

    return res


def validate_user_id(user_id: int) -> dict[str, Any]:
    """Validar se id do usuário que está sendo acessado é corresponde
    às credenciais providenciadas via jwt

    Returns:
        dict: {ok: bool, resp: Response | None}
    """
    res = {"ok": True, "resp": None}

    curr_user = get_current_user()

    if user_id != curr_user.id:
        res["ok"] = False
        res["resp"] = make_json_resp(
            ok=False,
            msg="As credenciais atuais não correspondem à url solicitada",
            status=401,
        )

    return res


def validate_json_data(
    json_data: dict[str, Any] | None, keys: Iterable[str]
) -> dict[str, Any]:
    """Validar se conteúdo JSON do request contém as chaves esperadas

    Returns:
        dict: {ok:bool, resp: Response | None}
    """
    res = {"ok": True, "resp": None}

    if not json_data:
        res["ok"] = False
        res["resp"] = make_json_resp(
            ok=False, msg=f"Os campos {keys} são obrigatórios"
        )
        return res

    errs = []
    for key in keys:
        val = json_data.get(key)
        if not val:
            errs.append(f"{key} é obrigatório")

    if errs:
        res["ok"] = False
        res["resp"] = make_json_resp(ok=False, msg=errs)

    return res
