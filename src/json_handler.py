from typing import Any


class JsonHandler:
    def __init__(self) -> None:
        pass

    def valdidate_keys(
        self, data: dict[Any, Any] | None, keys: list[Any]
    ) -> dict[str, Any]:
        res = {"ok": True, "erros": []}

        if not data:
            res["ok"] = False
            res["erros"] = [f"O campo {k} é obrigatório" for k in keys]
            return res

        errs = []
        for key in keys:
            val = data.get(key)

            if isinstance(val, str):
                val = val.replace(" ", "")

            if val in (None, ""):
                errs.append(f"O campo {key} é obrigatório")

        if errs:
            res["ok"] = False
            res["erros"] = errs
            return res

        return res
