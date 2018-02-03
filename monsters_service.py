from monsters_repo import MonstersRepo
from exceptions import *


class MonstersService:
    def __init__(self):
        self.repo = MonstersRepo()

    def find(self, name):
        return self.repo.find(name)

    def list(self):
        return self.repo.list()

    def create(self, monster):
        if monster.is_invalid():
            raise InvalidModelException

        xist = self.repo.find(monster.name)
        if xist is not None:
            raise ConflictException

        return self.repo.create(monster)

    def update(self, name, monster):
        if monster.is_invalid():
            raise InvalidModelException

        xist = self.repo.find(name)
        if xist is None:
            raise NotFoundException

        conflict = self.find(monster.name)
        if conflict is not None and name != conflict.name:
            raise ConflictException

        self.repo.update(name, xist.get_update_statement(monster))
        return monster

    def delete(self, name):
        if self.repo.find(name) is None:
            raise NotFoundException
        self.repo.delete(name)
