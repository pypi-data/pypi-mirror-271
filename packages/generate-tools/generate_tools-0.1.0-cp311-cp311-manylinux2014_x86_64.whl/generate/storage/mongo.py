from pymongo import MongoClient


class Mongo:
    def __init__(self, mongoUrl, mongoName):
        self.url = mongoUrl
        self.name = mongoName

        if self.url:
            self.mDb = MongoClient(self.url)
            if self.name:
                self._mongo = self.mDb[self.name]
            else:
                self._mongo = self.mDb["GenerateTools"]

    @property
    def mongo(self):
        return self._mongo

    def collection(self, name: str):
        return self._mongo[name]
