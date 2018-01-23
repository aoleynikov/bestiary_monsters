import json
from flask import Blueprint, request, Response
from models.skill import Skill
from monsters_service import MonstersService
from skills_service import SkillsService
from base_blueprint import build_response

skills_blueprint = Blueprint('skills_blueprint', __name__)


@skills_blueprint.route('/monsters/<monster_name>/skills', methods=['POST'])
def append_skill(monster_name):
    monster = MonstersService().find(monster_name)
    if monster is None:
        return Response(None, status=404)

    body = request.get_json()
    skill = Skill.from_document(body)
    result = SkillsService().append_skill(monster, skill)
    if result is None:
        return Response(None, status=409)
    else:
        return build_response(skill, 200)


@skills_blueprint.route('/monsters/<monster_name>/skills/<skill_name>', methods=['DELETE'])
def remove_skill(monster_name, skill_name):
    monster = MonstersService().find(monster_name)
    # Monster not found
    if monster is None:
        return Response(None, status=404)

    # Deleted skill not found
    if skill_name not in monster.skill_names():
        return Response(None, status=404)

    SkillsService().remove_skill(monster, skill_name)
    return Response(None, status=200)