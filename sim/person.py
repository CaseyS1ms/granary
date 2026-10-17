from config import HUNGER_RELIEF_WHEN_FED, HUNGER_GAINED_PER_TICK_UNFED, STARVATION_DAMAGE_PER_TICK, \
    REPRODUCTION_COOLDOWN, TICKS_PER_YEAR, RNG, BIRTH_CHANCE, MIN_FERTILE_AGE, MAX_FERTILE_AGE


class Person:

    def __init__(self, gender, tick=0, age=0):
        self.alive = True
        self.hunger = 0
        self.health = 100
        self.gender = gender
        self.tick_last_reproduction = None
        self.job = None
        self.max_age = RNG.randint(70, 110)
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

    def can_reproduce(self,birth_factor, tick=0, ):
        age = self.get_age_in_years(tick)
        if MIN_FERTILE_AGE <= age <= MAX_FERTILE_AGE and self.gender == 2 and self.hunger <= 50 and RNG.random() < BIRTH_CHANCE * birth_factor:
            if self.tick_last_reproduction is None or tick - self.tick_last_reproduction >= REPRODUCTION_COOLDOWN:
                self.tick_last_reproduction = tick
                # print(f"Person can reproduce with a birth factor of {birth_factor}")
                return True
            else:
                # print(f"Person can't reproduce yet, birth factor is {birth_factor}")
                return False

        else:
            # print(f"Person can't reproduce yet, birth factor is {birth_factor}")
            return False
