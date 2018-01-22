import json
from flask import Blueprint, request, Response
from models.monster import Monster
from monsters_service import MonstersService
from base_blueprint import build_response


monsters_blueprint = Blueprint('monsters', __name__)


@monsters_blueprint.route('/monsters', methods=['GET'])
def list_monsters():
    monsters = [m.to_json() for m in MonstersService().list()]
    return Response(json.dumps(monsters), content_type='application/json')


@monsters_blueprint.route('/monsters', methods=['POST'])
def create_monster():
    body = request.get_json()
    monster = Monster.from_document(body)
    result = MonstersService().create(monster)
    if result is None:
        return Response(None, status=409)
    else:
        return build_response(result, 201)


@monsters_blueprint.route('/monsters/<monster_name>', methods=['PUT'])
def update_monster(monster_name):
    body = request.get_json()
    monster = Monster.from_document(body)
    conflict = MonstersService().find(monster.name)
    if conflict is not None:
        return Response(None, status=409)
    result = MonstersService().update(monster_name, monster)
    if result is None:
        return Response(None, status=404)
    else:
        return build_response(result, 200)


@monsters_blueprint.route('/monsters/<monster_name>', methods=['DELETE'])
def delete_monster(monster_name):
    monster = MonstersService().find(monster_name)
    if monster is None:
        return Response(None, status=404)
    MonstersService().delete(monster)
    return Response(None, status=200)