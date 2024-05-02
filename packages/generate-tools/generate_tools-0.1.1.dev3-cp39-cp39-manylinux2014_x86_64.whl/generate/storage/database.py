import typing

from generate.exception import InvalidCollectionName

from .base import Base
from .collection import Collection


class Database(Collection):
    def __init__(self, name: str):
        super().__init__(name)

    def collection(self, collectionName: str) -> "Collection":
        if not collectionName:
            raise InvalidCollectionName()
        collect = Collection(collectionName)
        return collect
