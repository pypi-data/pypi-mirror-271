import typing


class Base(object):
    def __init__(self, name: str):
        super().__init__()
        self._baseName = name
        self._db: dict = {}
        self.aDb: typing.Optional[dict] = None

    def connect(self):
        self._db[self._baseName] = {}
        self.aDb = self._db[self._baseName]
        return self.aDb