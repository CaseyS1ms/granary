import random

from config import HUNGER_RELIEF_WHEN_FED, HUNGER_GAINED_PER_TICK_UNFED, STARVATION_DAMAGE_PER_TICK, \
    REPRODUCTION_COOLDOWN


class Person:

    def __init__(self, age, gender):
        self.alive = True
        self.hunger = 0
        self.health = 100
        self.age = age
        self.gender = gender
        self.tick_last_reproduction = None




    def eat(self):
        self.hunger = max(0, self.hunger - HUNGER_RELIEF_WHEN_FED)

    def increase_hunger(self):
        self.hunger = min(100, self.hunger + HUNGER_GAINED_PER_TICK_UNFED)

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        if self.health <= 0:
            self.alive = False


    def can_reproduce(self,tick):
        if self.age >= 18 and self.gender == 2:
            if self.hunger <= 50:
                if self.tick_last_reproduction is None:
                    self.tick_last_reproduction = tick
                    return True
                elif tick - self.tick_last_reproduction >= REPRODUCTION_COOLDOWN:
                    self.tick_last_reproduction = tick
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False



