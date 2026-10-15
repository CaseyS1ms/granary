import random

from sim.person import Person

from config import *


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

            if p.get_age_in_years(self.tick) > p.max_age:
                p.alive = False
                continue

            if p.get_age_in_years(self.tick) >= MIN_WORKING_AGE:
                p.job = random.choice(JOBS)
            if p.get_age_in_years(self.tick) >= MAX_WORKING_AGE:
                p.job = None


            if p.hunger >= 100:
                p.take_damage(STARVATION_DAMAGE_PER_TICK)

            if not p.alive:
                continue
            if self.food >= FOOD_PER_PERSON_PER_TICK:
                self.food -= FOOD_PER_PERSON_PER_TICK
                p.eat()
            else:
                p.increase_hunger()

            if p.job == "farmer" and p.hunger <= 70:
                self.food += FOOD_PRODUCED_PER_FARMER


            if p.can_reproduce(self.tick):
                newborns.append(Person(gender = random.choice([1,2]), tick = self.tick, age = 0))
                print("Newborn born")




        people = [p for p in self.people if p.alive] + newborns
        self.people = people

        self.tick += 1






