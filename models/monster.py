from models.creature import Creature
from models.validators import *

class Monster(Creature):
    def __init__(self, name, strength, dexterity, constitution, intelligence, wisdom, charisma, hp):
        Creature.__init__(self, strength, dexterity, constitution, intelligence, wisdom, charisma, hp)
        self.name = name
        self.__init_validators()

    def from_document(document):
        result = Monster(document['name'],
                         document['strength'],
                         document['dexterity'],
                         document['constitution'],
                         document['intelligence'],
                         document['wisdom'],
                         document['charisma'],
                         document['hit_points'])
        return result

    def __init_validators(self):
        self._validators.append(GreaterThanZeroValidator('strength', self))
