from flask import Flask, request, Response

from models.monster import Monster
from monsters_service import MonstersService

app = Flask(__name__)


@app.route('/')
def hello_world():
    return Response('Hello, World', status=200, content_type='text/plain')


@app.route('/monsters', methods=['GET'])
def list_monsters():
    monsters = [m.json_response() for m in MonstersService().list()]
    resp = '[' + ', '.join(monsters) + ']'
    return Response(resp, content_type='application/json')


@app.route('/monsters', methods=['POST'])
def create_monster():
    body = request.get_json()
    monster = Monster.from_document(body)
    result = MonstersService().create(monster)

    if result is None:
        return Response(None, status=409)  # Conflict
    else:
        return Response(result.json_response(), status=201)


@app.route('/monsters/<monster_name>', methods=['PUT'])
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
        return Response(monster.json_response(), status=200)


@app.route('/monsters/<monster_name>', methods=['DELETE'])
def delete_monster(monster_name):
    monster = MonstersService().find(monster_name)
    if monster is None:
        return Response(None, status=404)
    MonstersService().delete(monster)
    return Response(None, status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
