from monsters_repo import MonstersRepo


class SkillsService:
    def __init__(self):
        self.repo = MonstersRepo()

    def append_skill(self, monster, skill):
        if skill.is_invalid():
            return skill
        if skill.name in [s.name for s in monster.skills]:
            return None
        self.repo.append(monster, 'skills', skill)
        return skill
