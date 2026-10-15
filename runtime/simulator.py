import random

from sim.settlement import Settlement
from sim.person import Person

settlement = Settlement(people = [Person(age = random.randint(15,60), gender = random.randint(1,2)) for i in range(10)], food = 100)

for i in range(365):
    settlement.step()