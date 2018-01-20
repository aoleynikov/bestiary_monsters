class BaseValidator:
    def __init__(self, field_name, model):
        self.field_name = field_name
        self.model = model
        self.valid = True
        self.error_message = ''

    def validate(self):
        raise NotImplementedError()

    def _value(self):
        return self.model.__dict__[self.field_name]
