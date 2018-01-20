from models.validators.base_validator import BaseValidator


class NonEmptyValidator(BaseValidator):
    def __init__(self, field_name, model):
        BaseValidator.__init__(self, field_name, model)
        self.error_message = 'should not be empty'

    def validate(self):
        self.valid = self._value() is not None and len(self._value()) > 0
