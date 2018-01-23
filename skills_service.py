from monsters_repo import MonstersRepo


class SkillsService:
    def __init__(self):
        self.repo = MonstersRepo()

    def append_skill(self, monster, skill):
        if skill.is_invalid():
            return skill
        if skill.name in monster.skill_names():
            return None
        self.repo.append(monster, 'skills', skill)
        return skill

    def remove_skill(self, monster, skill_name):
        self.repo.remove_skill(monster, skill_name)