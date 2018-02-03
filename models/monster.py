from models.base_entity import BaseEntity
from models.validators import *
from models.skill import Skill
from models.movement import Movement
from models.action import Action


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
        self.movements = []
        self.actions = []

        self.__init_validators()

    @staticmethod
    def from_document(document):
        result = Monster(document.get('name', None),
                         document.get('strength', None),
                         document.get('dexterity', None),
                         document.get('constitution', None),
                         document.get('intelligence', None),
                         document.get('wisdom', None),
                         document.get('charisma', None),
                         document.get('hit_points', None))

        result.skills = [Skill.from_document(sd) for sd in document['skills']]
        result.movements = [Movement.from_document(md) for md in document['movements']]
        result.actions = [Action.from_document(ad) for ad in document['actions']]

        return result

    def to_json(self):
        result = super(Monster, self).to_json()
        result['skills'] = [s.to_json() for s in self.skills]
        result['movements'] = [m.to_json() for m in self.movements]
        result['actions'] = [a.to_json() for a in self.actions]
        return result

    def validate(self):
        super(Monster, self).validate()
        for skill in self.skills:
            skill.validate()
        for movement in self.movements:
            movement.validate()

    def is_invalid(self):
        self.validate()
        if self.errors:
            return True
        valid = True
        for s in self.skills:
            valid = valid and not s.is_invalid()
        for m in self.movements:
            valid = valid and not m.is_invalid()
        return not valid

    def skill_names(self):
        return [s.name for s in self.skills]

    def movement_types(self):
        return [m.type for m in self.movements]

    def get_update_statement(self, other):
        update_statement = {}
        self_json = self.to_json()
        other_json = other.to_json()
        for key in self_json.keys():
            if self_json[key] != other_json[key]:
                update_statement[key] = other_json[key]  # set value of second operand

        return {'$set': update_statement}

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

        self._validators.append(UniqueDependencyValidator('skills', self, lambda s: s.name))
        self._validators.append(UniqueDependencyValidator('movements', self, lambda m: m.type))
        self._validators.append(UniqueDependencyValidator('actions', self, lambda a: a.name))
