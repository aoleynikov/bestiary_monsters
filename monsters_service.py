from monsters_repo import MonstersRepo

class MonstersService:
    def __init__(self):
        self.repo = MonstersRepo()

    def find(self, name):
        return self.repo.find(name)

    def list(self):
        return self.repo.list()

    def create(self, monster):
        xist = self.repo.find(monster.name)
        if xist is None:
            return self.repo.create(monster)
        else:
            return None

    def update(self, name, monster):
        xist = self.repo.find(name)
        if xist is None:
            return None
        else:
            self.delete(xist)
            return self.create(monster)

    def delete(self, monster):
        self.repo.delete(monster)
