from models.validators.base_validator import BaseValidator


class GreaterThanZeroValidator(BaseValidator):
    def __init__(self, field_name, model):
        BaseValidator.__init__(self, field_name, model)
        self.error_message = 'should be greater than zero'

    def validate(self):
        value_str = self._value()
        if value_str is None:
            self.valid = False
            return
        val = 0
        try:
            val = int(value_str)
        except ValueError:
            self.valid = False
            self.error_message = 'should be an integer'
        self.valid = int(val) > 0
