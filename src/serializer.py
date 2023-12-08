from typing import Any, Iterable

from flask_sqlalchemy.pagination import Pagination
from sqlalchemy.inspection import inspect


class Serializer(object):
    def __init__(self, table: Any) -> None:
        self.inspector = inspect(table, raiseerr=True)
        self.cols = tuple([col.key for col in self.inspector.column_attrs])

    def serialize(self, obj: Any, ignore_attrs: list[str] = []):
        res: dict[Any, Any] = {}

        for col in self.cols:
            if col in ignore_attrs:
                continue

            if not hasattr(obj, col):
                continue

            res[col] = getattr(obj, col, None)

        return res

    def serialize_many(
        self, query: Iterable[Any], ignore_attrs: list[str] = []
    ):
        return [
            self.serialize(obj=obj, ignore_attrs=ignore_attrs) for obj in query
        ]

    def serialize_pagination(
        self, pagination: Pagination, ignore_attrs: list[str] = []
    ):
        data = [
            self.serialize(obj=item, ignore_attrs=ignore_attrs)
            for item in pagination.items
        ]

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
