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
        doc = monster.to_json()
        self.collection.insert(doc)
        return monster

    def find(self, name):
        doc = self.collection.find_one({'name': name})
        if doc is None:
            return None
        else:
            return Monster.from_document(doc)

    def append(self, monster, field_name, item):
        self.collection.update({'name': monster.name}, {'$push': {field_name: item.to_json()}})

    def delete(self, monster):
        self.collection.remove({'name': monster.name})
        return None

    def remove_skill(self, monster, skill_name):
        self.collection.update({'name': monster.name}, {'$pull': {'skills': {'name': skill_name}}})
