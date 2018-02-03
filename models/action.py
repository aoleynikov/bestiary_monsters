from models.base_entity import BaseEntity
from models.validators import *


class Action(BaseEntity):
    def __init__(self, name, description):
        BaseEntity.__init__(self)
        self.name = name
        self.description = description
        self.__init_validators()

    @staticmethod
    def from_document(document):
        return Action(document.get('name', None),
                      document.get('description', None))

    def __init_validators(self):
        self._validators.append(RequiredValidator('name', self))
        self._validators.append(NonEmptyValidator('name', self))
