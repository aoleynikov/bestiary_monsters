from models.base_entity import BaseEntity
from models.validators import *


class Creature(BaseEntity):
    def __init__(self, strength, dexterity, constitution, intelligence, wisdom, charisma, hp):
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.hit_points = hp
        BaseEntity.__init__(self)
        self.__init_validators()

    def __init_validators(self):
        self._validators.append(RequiredValidator('strength', self))
        self._validators.append(GreaterThanZeroValidator('strength', self))

        self._validators.append(RequiredValidator('dexterity', self))
        self._validators.append(GreaterThanZeroValidator('dexterity', self))

        self._validators.append(RequiredValidator('constitution', self))
        self._validators.append(GreaterThanZeroValidator('constitution', self))

        self._validators.append(RequiredValidator('intelligence', self))
        self._validators.append(GreaterThanZeroValidator('intelligence', self))

        self._validators.append(RequiredValidator('wisdom', self))
        self._validators.append(GreaterThanZeroValidator('wisdom', self))

        self._validators.append(RequiredValidator('charisma', self))
        self._validators.append(GreaterThanZeroValidator('charisma', self))

        self._validators.append(RequiredValidator('hit_points', self))
        self._validators.append(GreaterThanZeroValidator('hit_points', self))
