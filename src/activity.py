from utils import get_fitness

class activity:

    def __init__(self, room, time, facilitator, fitness):
        self.room = room
        self.time = time
        self.facilitator = facilitator
        self.fitness = utils.get_fitness(room, time, facilitator)