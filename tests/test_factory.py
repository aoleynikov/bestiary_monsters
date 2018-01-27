from random import *
from faker import Faker
from models.monster import Monster
from models.skill import Skill
from models.movement import Movement
from models.action import Action


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


class MovementInitializer(BaseInitializer):
    def instantiate(self):
        allowed_types = ['', 'walk', 'swim', 'fly', 'run', 'climb', 'crawl']
        selected_type = allowed_types[randint(0, len(allowed_types) - 1)]
        return Movement(selected_type, randint(1, 120))


class ActionInitializer(BaseInitializer):
    def instantiate(self):
        name = self.faker.word()
        description = self.faker.text()
        return Action(name, description)


class InitializerNotFound(BaseException):
    pass


class TestFactory:
    def __init__(self):
        self.__initializers = dict()
        self.__initializers['monster'] = MonsterInitializer()
        self.__initializers['skill'] = SkillInitializer()
        self.__initializers['movement'] = MovementInitializer()
        self.__initializers['action'] = ActionInitializer()

    def build(self, key):
        if key not in self.__initializers.keys():
            raise InitializerNotFound
        initializer = self.__initializers[key]
        return initializer.instantiate()
