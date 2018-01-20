from models.validators.base_validator import BaseValidator


class RequiredValidator(BaseValidator):
    def __init__(self, field_name, model):
        BaseValidator.__init__(self, field_name, model)
        self.error_message = 'is required'

    def validate(self):
        self.valid = self._value() is not None
