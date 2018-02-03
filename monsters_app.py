import json
from flask import Flask, request, Response
from models.monster import Monster
from monsters_service import MonstersService
from exceptions import *

app = Flask(__name__)


def build_response(operation, model, success_code):
    try:
        result = operation()
    except ConflictException:
        return Response(None, status=409)
    except NotFoundException:
        return Response(None, status=404)
    except InvalidModelException:
        return Response(json.dumps(model.to_json()), status=400)
    if result is None:
        return Response(None, status=success_code)
    else:
        return Response(json.dumps(result.to_json()), status=success_code)


@app.route('/health', methods=['GET'])
def healthcheck():
    return "Monsters alive!"


@app.route('/', methods=['GET'])
def list_monsters():
    monsters = [m.to_json() for m in MonstersService().list()]
    return Response(json.dumps(monsters), content_type='application/json')


@app.route('/', methods=['POST'])
def create_monster():
    body = request.get_json()
    monster = Monster.from_document(body)
    return build_response(lambda: MonstersService().create(monster), monster, 201)


@app.route('/<monster_name>', methods=['PUT'])
def update_monster(monster_name):
    body = request.get_json()
    monster = Monster.from_document(body)
    return build_response(lambda: MonstersService().update(monster_name, monster), monster, 200)


@app.route('/<monster_name>', methods=['DELETE'])
def delete_monster(monster_name):
    return build_response(lambda: MonstersService().delete(monster_name), None, 200)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
