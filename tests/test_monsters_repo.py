from monsters_repo import MonstersRepo

class TestMonstersRepo(MonstersRepo):
    def delete_all(self):
        self.collection.remove({})
        return None
