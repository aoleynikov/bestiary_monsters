import unittest
from tests.test_factory import TestFactory


class ValidationTest(unittest.TestCase):
    def setUp(self):
        self.factory = TestFactory()

    def test_strength_greater_than_zero_validation(self):
        monster = self.factory.build('monster')
        monster.strength = -1

        monster.validate()

        assert len(monster.errors.keys()) == 1

    def tearDown(self):
        pass
