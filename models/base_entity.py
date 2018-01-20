import json


class BaseEntity:
    def json_response(self):
        d = self.__dict__
        d.pop('_id', None)
        return json.dumps(d)
