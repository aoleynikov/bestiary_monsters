from random import *
from faker import Faker
from models.monster import Monster
from models.skill import Skill


class BaseInitializer:
    def __init__(self):
        self.faker = Faker()

    def instantiate(self):
        raise NotImplementedError()


class MonsterInitializer(BaseInitializer):
    def instantiate(self):
        name = self.faker.word()
        return Monster(name,
                       randint(1, 30),  # strength
                       randint(1, 30),  # dexterity
                       randint(1, 30),  # constitution
                       randint(1, 30),  # intelligence
                       randint(1, 30),  # wisdom
                       randint(1, 30),  # charisma
                       randint(1, 30))  # hp


class SkillInitializer(BaseInitializer):
    def instantiate(self):
        name = self.faker.word()
        description = self.faker.text()
        bonus = randint(-2, 5)
        return Skill(name, description, bonus)


class InitializerNotFound(BaseException):
    pass


class TestFactory:
    def __init__(self):
        self.__initializers = dict()
        self.__initializers['monster'] = MonsterInitializer()
        self.__initializers['skill'] = SkillInitializer()

    def build(self, key):
        if key not in self.__initializers.keys():
            raise InitializerNotFound
        initializer = self.__initializers[key]
        return initializer.instantiate()
