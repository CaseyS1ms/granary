
import matplotlib.pyplot as plt

from config import RNG, TICKS_PER_YEAR
from sim.settlement import Settlement
from sim.person import Person

settlement = Settlement(people = [Person(age = RNG.randint(5,60), gender = RNG.randint(1,2)) for i in range(100)], food = 1000)

for i in range(TICKS_PER_YEAR * 2):
    settlement.step()
    if not settlement.people:
        break

h = settlement.history
years = [t / TICKS_PER_YEAR for t in h["tick"]]

fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

axes[0].plot(years, h["population"])
axes[0].set_ylabel("Population")

axes[1].plot(years, h["food"], color="tab:green")
axes[1].set_ylabel("Food stock")

axes[2].plot(years,h["deaths"], color="tab:red")
axes[2].set_ylabel("Deaths")
axes[2].set_xlabel("Year")




fig.tight_layout()
plt.show()