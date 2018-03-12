import unittest
import json
import copy
from monsters_app import app
from tests.test_monsters_repo import TestMonstersRepo
from tests.test_factory import TestFactory
from tests.test_user_manager import TestUserManager


class MonstersTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.token = TestUserManager.create_and_authorize()

    def setUp(self):
        self.repo = TestMonstersRepo()
        self.client = app.test_client(self)
        self.factory = TestFactory()

    def test_monster_creation(self):
        monster = self.factory.build('monster')

        response = self.client.post('/',
                                    data=json.dumps(monster.to_json()),
                                    content_type='application/json',
                                    headers={'Authorization': 'Bearer ' + MonstersTest.token})

        assert response.status_code == 201
        assert self.repo.find(monster.name) is not None

    def test_monster_duplication_protection(self):
        monster = self.factory.build('monster')
        self.repo.create(monster)

        response = self.client.post('/',
                                    data=json.dumps(monster.to_json()),
                                    content_type='application/json',
                                    headers={'Authorization': 'Bearer ' + MonstersTest.token})

        assert response.status_code == 409  # Conflict

    def test_empty_monsters_list(self):
        response = self.client.get('/').data.decode()
        assert '[]' in response

    def test_non_empty_monsters_list(self):
        monsters = []
        for i in range(3):
            monster = self.factory.build('monster')
            monsters.append(monster)
            self.repo.create(monster)

        response = self.client.get('/').data.decode()
        json_response = json.loads(response)

        assert len(json_response) == 3
        uniq = set([jr['name'] for jr in json_response])
        assert len(uniq) == 3
        for jr in json_response:
            found = list(filter(lambda m: m.name == jr['name'], monsters))
            assert len(found) == 1

    def test_delete_non_existent_monster(self):
        response = self.client.delete('/not_existing',
                                      headers={'Authorization': 'Bearer ' + MonstersTest.token})
        assert response.status_code == 404

    def test_delete_existing_monster(self):
        monster = self.factory.build('monster')
        self.repo.create(monster)

        response = self.client.delete('/' + monster.name,
                                      headers={'Authorization': 'Bearer ' + MonstersTest.token})

        assert response.status_code == 200
        assert self.repo.find(monster.name) is None

    def test_update_non_existing_monster(self):
        monster = self.factory.build('monster')
        response = self.client.put('/not_existing',
                                   data=json.dumps(monster.to_json()),
                                   content_type='application/json',
                                   headers={'Authorization': 'Bearer ' + MonstersTest.token})

        assert response.status_code == 404

    def test_update_existing_monster(self):
        monster = self.factory.build('monster')
        monster.skills.append(self.factory.build('skill'))
        self.repo.create(monster)
        new_monster_data = self.factory.build('monster')
        new_monster_data.skills.append(monster.skills[0])
        response = self.client.put('/' + monster.name,
                                   data=json.dumps(new_monster_data.to_json()),
                                   content_type='application/json',
                                   headers={'Authorization': 'Bearer ' + MonstersTest.token})

        assert response.status_code == 200
        assert self.repo.find(monster.name) is None
        assert self.repo.find(new_monster_data.name) is not None
        assert len(self.repo.find(new_monster_data.name).skills) > 0

    def test_update_with_name_conflict(self):
        monster = self.factory.build('monster')
        old_monster_name = monster.name
        self.repo.create(monster)
        xist = self.factory.build('monster')
        self.repo.create(xist)
        monster.name = xist.name
        monster.strength = 31
        response = self.client.put('/' + old_monster_name,
                                   data=json.dumps(monster.to_json()),
                                   content_type='application/json',
                                   headers={'Authorization': 'Bearer ' + MonstersTest.token})

        assert response.status_code == 409  # Conflict
        assert self.repo.find(monster.name).strength != 31

    def test_create_monster_with_negative_strength(self):
        monster = self.factory.build('monster')
        monster.strength = -1

        response = self.client.post('/',
                                    data=json.dumps(monster.to_json()),
                                    content_type='application/json',
                                    headers={'Authorization': 'Bearer ' + MonstersTest.token})

        assert response.status_code == 400

    def test_create_monster_without_strength(self):
        monster = self.factory.build('monster')
        monster.strength = None

        response = self.client.post('/',
                                    data=json.dumps(monster.to_json()),
                                    content_type='application/json',
                                    headers={'Authorization': 'Bearer ' + MonstersTest.token})

        assert response.status_code == 400

    def test_create_monster_without_name(self):
        monster = self.factory.build('monster')
        monster.name = None

        response = self.client.post('/',
                                    data=json.dumps(monster.to_json()),
                                    content_type='application/json',
                                    headers={'Authorization': 'Bearer ' + MonstersTest.token})

        assert response.status_code == 400

    def test_create_monster_with_empty_name(self):
        monster = self.factory.build('monster')
        monster.strength = ''

        response = self.client.post('/',
                                    data=json.dumps(monster.to_json()),
                                    content_type='application/json',
                                    headers={'Authorization': 'Bearer ' + MonstersTest.token})

        assert response.status_code == 400

    def test_monster_update_statement_property(self):
        monster = self.factory.build('monster')
        other = copy.copy(monster)
        other.name = 'other_name'
        update_statement = monster.get_update_statement(other)
        assert update_statement == {'$set': {'name': 'other_name'}}

    def test_monster_update_statement_different_skill_set(self):
        monster = self.factory.build('monster')
        monster.skills.append(self.factory.build('skill'))
        monster.skills.append(self.factory.build('skill'))
        monster.skills.append(self.factory.build('skill'))
        other = copy.copy(monster)
        other.skills = []
        update_statement = monster.get_update_statement(other)
        assert update_statement == {'$set': {'skills': []}}

    def test_monster_with_invalid_skill(self):
        monster = self.factory.build('monster')
        skill = self.factory.build('skill')
        skill.name = None
        monster.skills.append(skill)

        response = self.client.post('/',
                                    data=json.dumps(monster.to_json()),
                                    content_type='application/json',
                                    headers={'Authorization': 'Bearer ' + MonstersTest.token})

        assert response.status_code == 400
        assert 'errors' in json.loads(response.data)['skills'][0].keys()

    def test_should_fail_with_repeating_skill_names(self):
        monster = self.factory.build('monster')
        skill = self.factory.build('skill')
        monster.skills.append(skill)
        monster.skills.append(skill)

        response = self.client.post('/',
                                    data=json.dumps(monster.to_json()),
                                    content_type='application/json',
                                    headers={'Authorization': 'Bearer ' + MonstersTest.token})
        assert response.status_code == 400

    def test_should_fail_with_repeating_movement_types(self):
        monster = self.factory.build('monster')
        movement = self.factory.build('movement')
        monster.movements.append(movement)
        monster.movements.append(movement)

        response = self.client.post('/',
                                    data=json.dumps(monster.to_json()),
                                    content_type='application/json',
                                    headers={'Authorization': 'Bearer ' + MonstersTest.token})
        assert response.status_code == 400

    def test_should_fail_with_repeating_movement_types(self):
        monster = self.factory.build('monster')
        action = self.factory.build('action')
        monster.actions.append(action)
        monster.actions.append(action)

        response = self.client.post('/',
                                    data=json.dumps(monster.to_json()),
                                    content_type='application/json',
                                    headers={'Authorization': 'Bearer ' + MonstersTest.token})
        assert response.status_code == 400

    def test_should_not_erase_dependencies_on_property_update(self):
        monster = self.factory.build('monster')
        monster.skills.append(self.factory.build('skill'))
        monster.movements.append(self.factory.build('movement'))
        monster.actions.append(self.factory.build('action'))
        self.repo.create(monster)
        monster.strength = 31
        response = self.client.put('/' + monster.name,
                                   data=json.dumps(monster.to_json()),
                                   content_type='application/json',
                                   headers={'Authorization': 'Bearer ' + MonstersTest.token})

        assert response.status_code == 200
        from_db = self.repo.find(monster.name)
        assert len(from_db.skills) == 1
        assert len(from_db.movements) == 1
        assert len(from_db.actions) == 1

    def tearDown(self):
        self.repo.delete_all()

    @classmethod
    def tearDownClass(cls):
        TestUserManager.clean_up(cls.token)


if __name__ == '__main__':
    unittest.main()