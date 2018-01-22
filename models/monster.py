from models.base_entity import BaseEntity
from models.validators import *
from models.skill import Skill


class Monster(BaseEntity):
    def __init__(self, name, strength, dexterity, constitution, intelligence, wisdom, charisma, hp):
        BaseEntity.__init__(self)
        self.name = name
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.hit_points = hp

        self.skills = []

        self.__init_validators()

    def from_document(document):
        result = Monster(document.get('name', None),
                         document.get('strength', None),
                         document.get('dexterity', None),
                         document.get('constitution', None),
                         document.get('intelligence', None),
                         document.get('wisdom', None),
                         document.get('charisma', None),
                         document.get('hit_points', None))

        if 'skills' in document.keys():
            result.skills = [Skill.from_document(sd) for sd in document['skills']]

        return result

    def to_json(self):
        result = super(Monster, self).to_json()
        result['skills'] = [s.to_json() for s in self.skills]
        return result


    def __init_validators(self):
        self._validators.append(NonEmptyValidator('name', self))

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