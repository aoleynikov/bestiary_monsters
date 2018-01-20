from random import *

from models.monster import Monster


class BaseInitializer:
    def instantiate(self):
        raise NotImplementedError()


class MonsterInitializer(BaseInitializer):
    def instantiate(self):
        name = 'test_monster_' + randint(0, 65000).__str__()

        return Monster(name,
                       randint(0, 30),  # strength
                       randint(0, 30),  # dexterity
                       randint(0, 30),  # constitution
                       randint(0, 30),  # intelligence
                       randint(0, 30),  # wisdom
                       randint(0, 30),  # charisma
                       randint(0, 30))  # hp


class InitializerNotFound(BaseException):
    pass


class TestFactory:
    def __init__(self):
        self.__initializers = dict()
        self.__initializers['monster'] = MonsterInitializer()

    def build(self, key):
        if key not in self.__initializers.keys():
            raise InitializerNotFound
        initializer = self.__initializers[key]
        return initializer.instantiate()
