
class Collection:
    def __init__(
        self,
        nameCollection: str,
        db: dict,
        baseName: str,
        aDb: dict
    ):
        self._nameCollect = nameCollection
        self.aDb = aDb
        self._db = db
        self._baseName = baseName
        if not self.aDb:
            self._db[self._baseName] = {}
            self.aDb = self._db[self._baseName]
            self.aDb[self._nameCollect] = {}
            self._collection = self.aDb[self._nameCollect]
        else:
            self.aDb[self._nameCollect] = {}
            self._collection = self.aDb[self._nameCollect]

    def findMany(self, target: str):
        try:
            data = self._collection[target]
            return data
        except KeyError:
            return None

    def findFirst(self, data: dict):
        arrayNull = []
        keys = data.keys()
        # values = data.values()
        if len(keys) > 1:
            for key, value in data.__dict__.items():
                try:
                    data = self._collection[key]
                    if data == value:
                        print(data)
                        arrayNull.append(data)
                except KeyError:
                    pass
            return arrayNull
        else:
            try:
                data = self._collection[keys[0]]
                return data
            except KeyError:
                return None
