import unittest
import json
from monsters_app import app
from tests.test_monsters_repo import TestMonstersRepo
from tests.test_factory import TestFactory


class SkillsTest(unittest.TestCase):
    def setUp(self):
        self.repo = TestMonstersRepo()
        self.client = app.test_client(self)
        self.factory = TestFactory()

    def test_adding_skill_to_monster(self):
        monster = self.factory.build('monster')
        skill = self.factory.build('skill')
        self.repo.create(monster)

        response = self.client.post('/monsters/' + monster.name + '/skills',
                                    data=json.dumps(skill.to_json()),
                                    content_type='application/json')

        assert response.status_code == 200
        from_mongo = self.repo.find(monster.name)
        assert len(from_mongo.skills) == 1
        assert from_mongo.skills[0].name == skill.name

    def test_adding_skill_to_not_existing_monster(self):
        skill = self.factory.build('skill')
        response = self.client.post('/monsters/not_existing/skills',
                                    data=json.dumps(skill.to_json()),
                                    content_type='application/json')
        assert response.status_code == 404

    def test_adding_the_same_skill(self):
        monster = self.factory.build('monster')
        skill = self.factory.build('skill')
        self.repo.create(monster)
        self.repo.append(monster, 'skills', skill)

        response = self.client.post('/monsters/' + monster.name + '/skills',
                                    data=json.dumps(skill.to_json()),
                                    content_type='application/json')

        assert response.status_code == 409

    def tearDown(self):
        self.repo.delete_all()