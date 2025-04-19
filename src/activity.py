from data import rooms, activities, times, facilitators, activity_info
from collections import defaultdict

class activity:

    def __init__(self, id, room, time, facilitator):
        self.id = id                    # activity name
        self.room = room                # the room in which the activity takes place
        self.time = time                # the timeslot of the activity
        self.facilitator = facilitator  # facilitator for the activity

    @staticmethod    
    def same_room_and_time_fitness(acs: list['activity']) -> float:
        fitness_total = 0.0
        room_schedule = defaultdict(lambda: defaultdict(lambda: 0))

        # saturate room->timeslot->count mapping with data
        for ac in acs: room_schedule[ac.room][ac.time] += 1

        # calculate fitness
        for room, timeslot_dict in room_schedule.items():
            for count in timeslot_dict.values():
                if count > 1: fitness_total -= 0.5 * count

        return fitness_total
    
    @staticmethod
    def room_size_fitness(ac: 'activity', ac_dict: dict[activity_info], room_dict: dict[str]) -> float:
        ac_info: activity_info = ac_dict[ac.id]
        expected_enrlmnt = ac_info.expected_enrollment
        room_capacity = room_dict[ac.room]

        if expected_enrlmnt > room_capacity:       return -0.5
        elif expected_enrlmnt * 3 < room_capacity: return -0.2
        elif expected_enrlmnt * 6 < room_capacity: return -0.4
        else:                                      return  0.3

    @staticmethod
    def preferred_facilitator_fitness(ac: 'activity', ac_dict: dict[activity_info]) -> float:
        ac_info: activity_info = ac_dict[ac.id]
        preferred = ac_info.preferred_facilitators
        other = ac_info.facilitators
        actual = ac.facilitator

        if actual in preferred: return  0.5
        elif actual in other:   return  0.2
        else:                   return -0.1

    @staticmethod
    def facilitator_load_timeslot_fitness(acs: list['activity']) -> float:
        fitness_total = 0.0
        facilitator_schedule = defaultdict(lambda: defaultdict(lambda: 0))

        # saturate facilitator->timeslot->count mapping with data
        for ac in acs: facilitator_schedule[ac.facilitator][ac.time] += 1

        # calculate fitness
        for facilitator, timeslot_dict in facilitator_schedule.items():
            for count in timeslot_dict.values():
                if count == 1:   fitness_total += 0.2
                elif count > 1:  fitness_total -= 0.2

        return fitness_total
    
    @staticmethod
    def facilitator_load_num_oversee_fitness(acs: list['activity']) -> float:
        num_oversee_dict = defaultdict(lambda: 0)
        fitness_total = 0.0

        for ac in acs: num_oversee_dict[ac.facilitator] += 1

        for fac_name, fac_ac_count in num_oversee_dict.items():
            if fac_name == 'Tyler' and fac_ac_count < 2: fitness_total += 0
            elif 1 <= fac_ac_count <= 2:                 fitness_total -= 0.4
            elif fac_ac_count > 4:                       fitness_total -= 0.5
        
        return fitness_total
    
    @staticmethod
    def facilitator_load_consecutive_oversee(acs: list['activity']) -> float:
        fitness_total = 0.0
        facilitator_schedule = defaultdict(lambda: defaultdict(lambda: 0))

        # saturate facilitator->timeslot->count mapping with data
        for ac in acs: facilitator_schedule[ac.facilitator][ac.time] += 1

        # calculate fitness
        for facilitator, timeslot_dict in facilitator_schedule.items():
            occupied_times = sorted(timeslot_dict.keys())
            previous_timeslot = occupied_times[0]
            for i in range(1, len(occupied_times)):
                current_timeslot = occupied_times[i]
                if current_timeslot - previous_timeslot == 1:
                    fitness_total -= 0.5
                previous_timeslot = current_timeslot
        
        return fitness_total


    @staticmethod
    def activity_specific_fitness(acs: list['activity']) -> float:

        # if using a different dataset, skip this function
        activity_names = [ac.id for ac in acs]
        if ("SLA100A" not in activity_names or "SLA100B" not in activity_names or
            "SLA191A" not in activity_names or "SLA191B" not in activity_names):
            return 0.0

        fitness_total = 0.0

        # helper functions
        def get_delta_hours(ac1: 'activity', ac2: 'activity') -> int:
            return abs(ac1.time - ac2.time)
        def is_consecutive(ac1: 'activity', ac2: 'activity') -> bool:
            return get_delta_hours(ac1, ac2) == 1
        def is_coincident(ac1: 'activity', ac2: 'activity') -> bool:
            return get_delta_hours(ac1, ac2) == 0
        def roman_beach_predicate(ac: 'activity') -> bool:
            return ac.room.split()[0] in ("Roman", "Beach")
        
        sla100a = list(filter(lambda e: e.id == "SLA100A", acs))[0]
        sla100b = list(filter(lambda e: e.id == "SLA100B", acs))[0]
        sla191a = list(filter(lambda e: e.id == "SLA191A", acs))[0]
        sla191b = list(filter(lambda e: e.id == "SLA191B", acs))[0]


        if get_delta_hours(sla100a, sla100b) > 4: fitness_total += 0.5
        elif is_coincident(sla100a, sla100b):     fitness_total -= 0.5

        if get_delta_hours(sla191a, sla191b) > 4: fitness_total += 0.5
        elif is_coincident(sla191a, sla191b):     fitness_total -= 0.5

        for sla100 in (sla100a, sla100b):
            for sla191 in (sla191a, sla191b):
                if is_consecutive(sla100, sla191):
                    fitness_total += (0.5 if
                                      roman_beach_predicate(sla100) and roman_beach_predicate(sla191) 
                                      else -0.4)
                if is_consecutive(sla100, sla191):   fitness_total += 0.25
                elif is_coincident(sla100, sla191):  fitness_total -= 0.25
        
        return fitness_total
        


        






