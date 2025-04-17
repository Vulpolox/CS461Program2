from . import data

class activity:

    def __init__(self, id, room, time, facilitator):
        self.id = id                    # activity name
        self.room = room                # the room in which the activity takes place
        self.time = time                # the timeslot of the activity
        self.facilitator = facilitator  # facilitator from a file
        self.fitness = 0                # fitness is initialized to 0 per the directions


    def calculate_fitness(self):
        pass