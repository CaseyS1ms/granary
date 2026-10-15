import random

from sim.person import Person

from config import FOOD_PER_PERSON_PER_TICK, HUNGER_RELIEF_WHEN_FED, HUNGER_GAINED_PER_TICK_UNFED, \
    STARVATION_DAMAGE_PER_TICK


class Settlement:

    def __init__(self, people, food):
        self.food = food
        self.people = people
        self.tick = 0


    @property
    def population(self):
        return sum(1 for p in self.people if p.alive)



    def step(self):

        newborns = []

        for p in self.people:

            if p.hunger >= 100:
                p.take_damage(STARVATION_DAMAGE_PER_TICK)

            if not p.alive:
                continue
            if self.food >= FOOD_PER_PERSON_PER_TICK:
                self.food -= FOOD_PER_PERSON_PER_TICK
                p.eat()
            else:
                p.increase_hunger()

            if p.can_reproduce(self.tick):
                newborns.append(Person(age = 0, gender = random.choice([1,2])))




        people = [p for p in self.people if p.alive] + newborns
        self.people = people

        self.tick += 1






