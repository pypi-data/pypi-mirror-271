import typing

from generate.exception import InvalidCollectionName

from .collection import Collection


class Database(object):
    def __init__(self, name: str):
        super().__init__()
        self._baseName = name
        self._db: dict = {}
        self.aDb: typing.Optional[dict] = None

    def connect(self):
        self._db[self._baseName] = {}
        self.aDb = self._db[self._baseName]
        return self.aDb

    def collection(self, collectionName: str) -> "Collection":
        if not collectionName:
            raise InvalidCollectionName()
        collect = Collection(
            nameCollection=collectionName,
            db=self._db,
            baseName=self._baseName,
            aDb=self.aDb
        )
        return collect
