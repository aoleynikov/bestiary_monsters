from pymongo import MongoClient

from models.monster import Monster


class MonstersRepo():
    def __init__(self):
        client = MongoClient('mongo', 27017)
        self.collection = client.local['monsters']

    def list(self):
        all_docs = self.collection.find({})
        return map(lambda d: Monster.from_document(d), all_docs)

    def create(self, monster):
        self.collection.insert(monster.__dict__)
        return monster

    def find(self, name):
        doc = self.collection.find_one({'name': name})
        if doc is None:
            return None
        else:
            return Monster.from_document(doc)

    def delete(self, monster):
        self.collection.remove({'name': monster.name})
        return None