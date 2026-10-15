class Settlement:

    def __init__(self, population, food):
        self.population = population
        self.food = food



    def tick(self):
        self.food -= self.population
        


    def eat(self, amount):
        taken = min(amount, self.food)
        self.food -= taken
        return taken
