from models.base_entity import BaseEntity

class Creature(BaseEntity):
    def __init__(self, strength, dexterity, constitution, intelligence, wisdom, charisma, hp):
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.hit_points = hp
