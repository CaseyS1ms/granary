import math

from config import *
from sim.person import Person


class Settlement:

    def __init__(self, people, food):
        self.food = food
        self.people = people
        self.tick = 0
        self.deaths = 0
        self.history = {"tick": [], "food": [], "population": [], "deaths": [], "farmers": []}


    @property
    def population(self):
        return sum(1 for p in self.people if p.alive)

    def step(self):

        # print(f" Number Years of Food left - {math.floor(self._food_security())}")

        tick = self.tick

        if self.tick % 365 == 0:
            # print(f"Year {self.tick // 365} - {self.population} people, number of years of food left - {math.floor(self._food_security())}, birth factor - {self._birth_factor(self._food_security(), F_LO, F_HI)}")
            pass

        # AGING, DEATH AND ONE TIME JOB ASSIGNMENT
        for p in self.people:
            age = p.get_age_in_years(self.tick)
            if age > p.max_age:
                p.alive = False
                self.deaths += 1
                continue

            if p.health <= 0:
                p.alive = False
                self.deaths += 1
                continue

            if age > MAX_WORKING_AGE:
                chance = CHANCE_OF_DEATH_ADULT_PER_TICK
            else:
                chance = CHANCE_OF_DEATH_CHILD_PER_TICK

            if RNG.random() < chance:
                p.alive = False
                self.deaths += 1
                continue


            if age >= MIN_WORKING_AGE and p.job is None:
                p.job = RNG.choice(JOBS)
            if age >= MAX_WORKING_AGE:
                p.job = None

        living = [p for p in self.people if p.alive]

        # PRODUCTION
        active_farmers = 0
        for p in living:
            if p.job == "farmer" and p.hunger <= 70:
                active_farmers += 1

        self.food += FOOD_PRODUCED_PER_FARMER * min(active_farmers, W_MAX)

        # FOOD AND HUNGER
        for p in living:
            if self.food >= FOOD_PER_PERSON_PER_TICK:
                self.food -= FOOD_PER_PERSON_PER_TICK
                p.eat()
            else:
                p.increase_hunger()

            if p.hunger >= 100:
                p.take_damage(STARVATION_DAMAGE_PER_TICK)
                if not p.alive:
                    self.deaths += 1
                    continue

        alive = [p for p in living if p.alive]

        # REPRODUCTION

        factor = self._birth_factor(self._food_security(), F_LO, F_HI)

        newborns = [Person(gender = RNG.randint(1,2), tick = tick, age = 0) for p in alive
                        if p.can_reproduce(factor, tick)]


        self.people = alive + newborns
        self.plot()
        self.tick += 1

    def plot(self):
        self.history["tick"].append(self.tick)
        self.history["food"].append(self.food)
        self.history["population"].append(self.population)
        self.history["deaths"].append(self.deaths)
        self.history["farmers"].append(len([p for p in self.people if p.job == "farmer"]))


    def _food_per_person(self):
        return self.food / self.population



    def _food_security(self):
        if self.population == 0:
            return 0
        F = self.food / ((FOOD_PER_PERSON_PER_TICK * TICKS_PER_YEAR) * self.population)
        return F


    def _birth_factor(self,f, f_lo, f_hi):
        t = ( (f - f_lo) / (f_hi - f_lo) )
        return max(0.0, min(1.0, t))
