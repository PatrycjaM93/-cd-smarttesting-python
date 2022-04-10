from typing import Generic, Optional, Protocol, TypeVar

import typing_inspect
from bson import ObjectId
from marshmallow_dataclass import class_schema
from pymongo.collection import Collection
from pymongo.database import Database


class ModelProto(Protocol):
    id: Optional[str]


Model = TypeVar("Model", bound=ModelProto)


class MongoRepository(Generic[Model]):
    def __init__(self, database: Database) -> None:
        self._collection = Collection(database, self._collection_name)
        bases = typing_inspect.get_generic_bases(self)
        model_cls = typing_inspect.get_args(bases[0])[0]
        self._schema = class_schema(model_cls)()

    @property
    def _collection_name(self) -> str:
        raise NotImplementedError("Ustaw nazwę kolekcji w klasie potomnej")

    def get(self, model_id: str) -> Optional[Model]:
        document = self._collection.find_one({"_id": ObjectId(model_id)})
        if document:
            document["id"] = str(document.pop("_id"))
            return self._schema.load(document)
        else:
            return None

    def save(self, model: Model) -> str:
        json_repr = self._schema.dump(model)
        if model.id is None:
            result = self._collection.insert_one(json_repr)
            return str(result.inserted_id)
        else:
            result = self._collection.update_one(
                {"_id": ObjectId(model.id)}, {"$set": json_repr}, upsert=True
            )
            return str(result.upserted_id or model.id)
