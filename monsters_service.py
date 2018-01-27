from monsters_repo import MonstersRepo

class MonstersService:
    def __init__(self):
        self.repo = MonstersRepo()

    def find(self, name):
        return self.repo.find(name)

    def list(self):
        return self.repo.list()

    def create(self, monster):
        if monster.is_invalid():
            return monster
        xist = self.repo.find(monster.name)
        if xist is None:
            return self.repo.create(monster)
        else:
            return None

    def update(self, name, monster):
        if monster.is_invalid():
            return monster
        xist = self.repo.find(name)
        if xist is None:
            return None
        else:
            self.repo.update(name, xist.get_update_statement(monster))
            return monster

    def delete(self, monster):
        self.repo.delete(monster)
