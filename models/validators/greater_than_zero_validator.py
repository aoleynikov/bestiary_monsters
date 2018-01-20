from models.validators.base_validator import BaseValidator


class GreaterThanZeroValidator(BaseValidator):
    def __init__(self, field_name, model):
        BaseValidator.__init__(self, field_name, model)
        self.error_message = 'should be greater than zero'

    def validate(self):
        if self._value() > 0:
            return
        self.valid = False
