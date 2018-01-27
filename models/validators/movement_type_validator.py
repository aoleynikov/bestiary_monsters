from models.validators.base_validator import BaseValidator


class MovementTypeValidator(BaseValidator):
    def __init__(self, field_name, model):
        BaseValidator.__init__(self, field_name, model)
        self.error_message = "incorrect movement type"

    def validate(self):
        self.valid = self._value() in ['', 'walk', 'swim', 'fly', 'run', 'climb', 'crawl']
