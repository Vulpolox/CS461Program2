from activity import activity
import data
import random

class schedule:
    def __init__(self):
        self.activities = self.generate_schedule
        self.fitness = 0

    def generate_schedule(self):
        activity_names = list(data.activities.keys())
        room_names = list(data.rooms.keys())

        # for each activity, assign random times, rooms, and facilitators
        for activity_name in activity_names:
            activity_to_add = activity (
                id=activity_name,
                room=random.choice(room_names),
                time=random.choice(data.times),
                facilitator=random.choice(data.facilitators)
            )
        self.activities.append(activity_to_add)


    def calculate_fitness(self):
        for act in self.activities:
            pass
        




    