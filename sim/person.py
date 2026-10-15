import random

from config import HUNGER_RELIEF_WHEN_FED, HUNGER_GAINED_PER_TICK_UNFED, STARVATION_DAMAGE_PER_TICK, \
    REPRODUCTION_COOLDOWN, TICKS_PER_YEAR


class Person:

    def __init__(self, gender, tick = 0, age = 0):
        self.alive = True
        self.hunger = 0
        self.health = 100
        self.gender = gender
        self.tick_last_reproduction = None
        self.job = None
        self.max_age = random.randint(70, 110)
        self.birth_tick = tick - int(age * TICKS_PER_YEAR)




    def get_age_in_years(self, current_tick):
        return int((current_tick - self.birth_tick) / TICKS_PER_YEAR)


    def eat(self):
        self.hunger = max(0, self.hunger - HUNGER_RELIEF_WHEN_FED)

    def increase_hunger(self):
        self.hunger = min(100, self.hunger + HUNGER_GAINED_PER_TICK_UNFED)

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        if self.health <= 0:
            self.alive = False
            print("person died")


    def can_reproduce(self,tick = 0):
        if self.get_age_in_years(tick) >= 18 and self.gender == 2:
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










