from models.base_entity import BaseEntity
from models.validators import *


class Skill(BaseEntity):
    def __init__(self, name, description, bonus):
        BaseEntity.__init__(self)
        self.name = name
        self.description = description
        self.bonus = bonus
        self.__init_validators()

    @staticmethod
    def from_document(document):
        return Skill(document.get('name', None),
                     document.get('description', None),
                     document.get('bonus', None))

    def __init_validators(self):
        self._validators.append(RequiredValidator('name', self))
        self._validators.append(NonEmptyValidator('name', self))

        self._validators.append(RequiredValidator('bonus', self))
