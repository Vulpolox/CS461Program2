from activity import activity
import data
import functools
import random

class schedule:
    def __init__(self, activities: list[activity]):
        self.activities = activities
        self.total_fitness = sum([act.fitness for act in activities])

    @staticmethod
    def generate_schedule():
        schdl = schedule([])
        activity_names = list(data.activities.keys())
        room_names = list(data.rooms.keys())


        for activity_name in activity_names:
            activity_to_add = activity (
                id=activity_name,
                room=random.choice(room_names),
                time=random.choice(data.times),
                facilitator=random.choice(data.facilitators)
            )


    