import json
from flask import Response


def build_response(model, success_code):
    if model.is_invalid():
        return Response(json.dumps(model.errors), status=400)
    else:
        return Response(json.dumps(model.to_json()), status=success_code)