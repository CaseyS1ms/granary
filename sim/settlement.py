from config import FOOD_PER_PERSON_PER_TICK, HUNGER_RELIEF_WHEN_FED, HUNGER_GAINED_PER_TICK_UNFED, \
    STARVATION_DAMAGE_PER_TICK


class Settlement:

    def __init__(self, people, food):
        self.food = food
        self.people = people


    @property
    def population(self):
        return sum(1 for p in self.people if p.alive)



    def tick(self):
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


        people = [p for p in self.people if p.alive]
        self.people = people






