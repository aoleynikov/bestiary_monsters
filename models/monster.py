from models.creature import Creature
from models.validators import *

class Monster(Creature):
    def __init__(self, name, strength, dexterity, constitution, intelligence, wisdom, charisma, hp):
        Creature.__init__(self, strength, dexterity, constitution, intelligence, wisdom, charisma, hp)
        self.name = name
        self._validators.append(NonEmptyValidator('name', self))

    def from_document(document):
        result = Monster(document.get('name', None),
                         document.get('strength', None),
                         document.get('dexterity', None),
                         document.get('constitution', None),
                         document.get('intelligence', None),
                         document.get('wisdom', None),
                         document.get('charisma', None),
                         document.get('hit_points', None))
        return result
