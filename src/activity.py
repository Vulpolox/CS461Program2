from . import data

class activity:

    def __init__(self, id, room, time, facilitator, num_enrollment):
        self.id = id                    # activity name
        self.room = room                # the room in which the activity takes place
        self.time = time                # the timeslot of the activity
        self.facilitator = facilitator  # facilitator for the activity
        self.num_enrollment = num_enrollment

    @staticmethod
    def same_room_and_time_fitness(ac1: 'activity', ac2: 'activity') -> float:
        return -0.5 if (ac1.room == ac2.room and ac1.time == ac2.time) else 0.0
    @staticmethod
    def room_size_fitness(ac1: 'activity') -> str:
        pass
