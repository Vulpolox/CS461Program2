from schedule import schedule
from data import config
import heapq

class population:
    def __init__(self):
        self.population_size = config["population_size"]
        self.schedules = self.generate_schedules()

    def generate_schedules(self, amount: int):
        for i in range(amount):
            pass

        


