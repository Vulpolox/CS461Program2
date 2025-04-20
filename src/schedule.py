from activity import activity
import data
import random

class schedule:
    def __init__(self):
        self.activities = []
        self.fitness = 0.0

        self._generate_schedule()
        self._calculate_fitness()

    def _generate_schedule(self):
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


    def _calculate_fitness(self):
        ac_dict = data.activities
        room_dict = data.rooms

        fitness_total = sum (
            [activity.same_room_and_time_fitness(self.activities),
            activity.facilitator_load_timeslot_fitness(self.activities),
            activity.facilitator_load_num_oversee_fitness(self.activities),
            activity.facilitator_load_consecutive_oversee(self.activities),
            activity.activity_specific_fitness(self.activities)]
        )

        for ac in self.activities:
            fitness_total += sum (
                [activity.room_size_fitness(ac, ac_dict, room_dict),
                activity.preferred_facilitator_fitness(ac, ac_dict)]
            )
        
        self.fitness = round(fitness_total, 2)