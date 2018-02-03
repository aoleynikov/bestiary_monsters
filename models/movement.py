from models.base_entity import BaseEntity
from models.validators import *


class Movement(BaseEntity):
    def __init__(self, movement_type, speed):
        BaseEntity.__init__(self)
        self.type = movement_type
        self.speed = speed
        self.__init_validators()

    @staticmethod
    def from_document(document):
        return Movement(document.get('type', None),
                        document.get('speed', None))

    def __init_validators(self):
        self._validators.append(RequiredValidator('type', self))
        self._validators.append(MovementTypeValidator('type', self))

        self._validators.append(RequiredValidator('speed', self))
        self._validators.append(GreaterThanZeroValidator('speed', self))
