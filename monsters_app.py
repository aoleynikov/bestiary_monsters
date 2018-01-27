import json
from flask import Flask, request, Response
from models.monster import Monster
from monsters_service import MonstersService

app = Flask(__name__)


def build_response(model, success_code):
    if model.is_invalid():
        return Response(json.dumps(model.to_json()), status=400)
    else:
        return Response(json.dumps(model.to_json()), status=success_code)


@app.route('/', methods=['GET'])
def list_monsters():
    monsters = [m.to_json() for m in MonstersService().list()]
    return Response(json.dumps(monsters), content_type='application/json')


@app.route('/', methods=['POST'])
def create_monster():
    body = request.get_json()
    monster = Monster.from_document(body)
    result = MonstersService().create(monster)
    if result is None:
        return Response(None, status=409)
    else:
        return build_response(result, 201)


@app.route('/<monster_name>', methods=['PUT'])
def update_monster(monster_name):
    body = request.get_json()
    monster = Monster.from_document(body)
    conflict = MonstersService().find(monster.name)
    if conflict is not None and monster_name != conflict.name:
        return Response(None, status=409)
    result = MonstersService().update(monster_name, monster)
    if result is None:
        return Response(None, status=404)
    else:
        return build_response(result, 200)


@app.route('/<monster_name>', methods=['DELETE'])
def delete_monster(monster_name):
    monster = MonstersService().find(monster_name)
    if monster is None:
        return Response(None, status=404)
    MonstersService().delete(monster)
    return Response(None, status=200)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
