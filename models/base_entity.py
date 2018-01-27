import json


class BaseEntity:
    def __init__(self):
        self._validators = []
        self.errors = {}

    def to_json(self):
        d = self.__dict__.copy()
        hidden_fields = ['_id', '_validators']
        if not d['errors']:
            hidden_fields.append('errors')
        for field_name in hidden_fields:
            d.pop(field_name, None)
        return d

    def __eq__(self, other):
        return self.to_json() == other.to_json()

    def validate(self):
        self.errors = {}
        for v in self._validators:
            v.validate()

        invalid = filter(lambda x: not x.valid, self._validators)
        for v in invalid:
            if v.field_name not in self.errors.keys():
                self.errors[v.field_name] = []
            self.errors[v.field_name].append(v.error_message)

    def is_invalid(self):
        self.validate()
        return bool(self.errors)
