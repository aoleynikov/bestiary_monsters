from models.validators.base_validator import BaseValidator


class UniqueDependencyValidator(BaseValidator):
    def __init__(self, field_name, model, func):
        BaseValidator.__init__(self, field_name, model)
        self.func = func
        self.error_message = 'skill names should be unique'

    def validate(self):
        names = map(self.func, self._value())
        self.valid = len(set(names)) == len(self._value())
