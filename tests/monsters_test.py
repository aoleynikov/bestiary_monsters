import unittest
import json
from monsters_app import app
from tests.test_monsters_repo import TestMonstersRepo
from tests.test_factory import TestFactory


class MonstersTest(unittest.TestCase):
    def setUp(self):
        self.repo = TestMonstersRepo()
        self.client = app.test_client(self)
        self.factory = TestFactory()

    def test_health(self):
        response = self.client.get('/')
        assert 'Hello, World' in response.data.__str__()

    def test_monster_creation(self):
        monster = self.factory.build('monster')

        response = self.client.post('/monsters',
                                    data=json.dumps(monster.to_json()),
                                    content_type='application/json')

        assert response.status_code == 201
        assert self.repo.find(monster.name) is not None

    def test_monster_duplication_protection(self):
        monster = self.factory.build('monster')
        self.repo.create(monster)

        response = self.client.post('/monsters',
                                    data=json.dumps(monster.to_json()),
                                    content_type='application/json')

        assert response.status_code == 409  # Conflict

    def test_empty_monsters_list(self):
        response = self.client.get('/monsters').data.decode()
        assert '[]' in response

    def test_non_empty_monsters_list(self):
        monsters = []
        for i in range(3):
            monster = self.factory.build('monster')
            monsters.append(monster)
            self.repo.create(monster)

        response = self.client.get('/monsters').data.decode()
        json_response = json.loads(response)

        assert len(json_response) == 3
        uniq = set([jr['name'] for jr in json_response])
        assert len(uniq) == 3
        for jr in json_response:
            found = list(filter(lambda m: m.name == jr['name'], monsters))
            assert len(found) == 1

    def test_delete_non_existent_monster(self):
        response = self.client.delete('/monsters/not_existing')
        assert response.status_code == 404

    def test_delete_existing_monster(self):
        monster = self.factory.build('monster')
        self.repo.create(monster)

        response = self.client.delete('/monsters/' + monster.name)

        assert response.status_code == 200
        assert self.repo.find(monster.name) is None

    def test_update_non_existing_monster(self):
        monster = self.factory.build('monster')
        response = self.client.put('/monsters/not_existing',
                                   data=json.dumps(monster.to_json()),
                                   content_type='application/json')
        assert response.status_code == 404

    def test_update_existing_monster(self):
        monster = self.factory.build('monster')
        self.repo.create(monster)
        new_monster_data = self.factory.build('monster')
        response = self.client.put('/monsters/' + monster.name,
                                   data=json.dumps(new_monster_data.to_json()),
                                   content_type='application/json')

        assert response.status_code == 200
        assert self.repo.find(monster.name) is None
        assert self.repo.find(new_monster_data.name) is not None

    def test_update_with_name_conflict(self):
        monster = self.factory.build('monster')
        self.repo.create(monster)
        xist = self.factory.build('monster')
        self.repo.create(xist)
        monster.name = xist.name
        monster.strength = 31
        response = self.client.put('/monsters/' + monster.name,
                                   data=json.dumps(monster.to_json()),
                                   content_type='application/json')

        assert response.status_code == 409  # Conflict
        assert self.repo.find(monster.name).strength != 31

    def test_create_invalid_monster(self):
        monster = self.factory.build('monster')
        monster.strength = -1

        response = self.client.post('/monsters',
                                    data=json.dumps(monster.to_json()),
                                    content_type='application/json')

        assert response.status_code == 400

    def tearDown(self):
        self.repo.delete_all()

if __name__ == '__main__':
    unittest.main()