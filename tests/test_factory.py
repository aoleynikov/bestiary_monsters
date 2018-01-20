from random import *

from models.monster import Monster


class BaseInitializer:
    def instantiate(self):
        raise NotImplementedError()


class MonsterInitializer(BaseInitializer):
    def instantiate(self):
        name = 'test_monster_' + randint(0, 65000).__str__()

        return Monster(name,
                       randint(1, 30),  # strength
                       randint(1, 30),  # dexterity
                       randint(1, 30),  # constitution
                       randint(1, 30),  # intelligence
                       randint(1, 30),  # wisdom
                       randint(1, 30),  # charisma
                       randint(1, 30))  # hp


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
