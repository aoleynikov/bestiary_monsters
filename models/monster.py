from models.creature import Creature


class Monster(Creature):
    def __init__(self, name, strength, dexterity, constitution, intelligence, wisdom, charisma, hp):
        self.name = name
        Creature.__init__(self, strength, dexterity, constitution, intelligence, wisdom, charisma, hp)

    def from_document(document):
        result = Monster(document['name'],
                         document['strength'],
                         document['dexterity'],
                         document['constitution'],
                         document['intelligence'],
                         document['wisdom'],
                         document['charisma'],
                         document['hit_points'])
        return result