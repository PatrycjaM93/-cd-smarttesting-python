import functools
import json
from typing import Any, Hashable, Type, cast

from marshmallow import Schema
from marshmallow_dataclass import class_schema
from smarttesting.message import Message

__all__ = [
    "dataclass_dump",
    "dataclass_load",
]


def dataclass_dump(data: Any) -> str:
    return json.dumps(data, cls=Encoder)


def dataclass_load(data: Any) -> Any:
    return json.loads(data, object_hook=decoder)


class Encoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        try:
            dataclass_type: Hashable = cast(Hashable, type(o))
            schema = _get_schema_for_dataclass(dataclass_type)
        except TypeError:
            return json.JSONEncoder.default(self, o)
        else:
            dict_repr = schema.dump(o)
            dict_repr["__dataclass_name__"] = type(o).__name__
            return dict_repr


def decoder(obj: Any) -> Any:
    if "__dataclass_name__" in obj:
        dataclass_name = obj.pop("__dataclass_name__")
        dataclass = Message.subclass_for_name(dataclass_name)
        schema = _get_schema_for_dataclass(cast(Hashable, dataclass))
        return schema.load(obj)
    else:
        return obj


@functools.lru_cache(maxsize=None)
def _get_schema_for_dataclass(dataclass_obj: Type) -> Schema:
    """
    Funkcja budująca instancję schemę dla podanej klasy udekorowanej @dataclass.

    Schema jest bezstanowa, więc bezpieczne jest reużywanie obiektów.
    """
    schema_cls = class_schema(dataclass_obj)
    return schema_cls()
