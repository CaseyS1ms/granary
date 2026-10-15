from config import HUNGER_RELIEF_WHEN_FED, HUNGER_GAINED_PER_TICK_UNFED, STARVATION_DAMAGE_PER_TICK


class Person:

    def __init__(self,age):
        self.alive = True
        self.hunger = 0
        self.health = 100
        self.age = age


    def eat(self):
        self.hunger = max(0, self.hunger - HUNGER_RELIEF_WHEN_FED)

    def increase_hunger(self):
        self.hunger = min(100, self.hunger + HUNGER_GAINED_PER_TICK_UNFED)

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        if self.health <= 0:
            self.alive = False
