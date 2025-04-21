import sys
sys.path.append('src')

import unittest
from activity import activity
from data import activity_info

class FitnessTests(unittest.TestCase):

    def setUp(self):
        # activity info
        self.ac_dict = {
        "SLA100A": activity_info(
            expected_enrollment=25,
            preferred_facilitators={"John", "Emily"},
            other_facilitators={"Alice", "Claire"}
        ),
        "SLA100B": activity_info(
            expected_enrollment=50,
            preferred_facilitators={"Alice"},
            other_facilitators={"John", "Claire"}
        ),
        "SLA191A": activity_info(
            expected_enrollment=100,
            preferred_facilitators={"Bob"},
            other_facilitators={"Claire", "Hare"}
        ),
        "SLA191B": activity_info(
            expected_enrollment=75,
            preferred_facilitators={"Claire"},
            other_facilitators={"Alice", "Bob"}
        ),
        "CS441": activity_info(
            expected_enrollment=500,
            preferred_facilitators={"Hare"},
            other_facilitators={"Bob", "John"}
        )
    }

        # room dictionary
        self.room_dict = {
            "Room1": 30,   # Room1 can hold 30 people
            "Room2": 50,   # Room2 can hold 50 people
            "Room3": 1000, # Big Room
            "Room4": 5     # Tiny room
        }

        # Activities (with facilitator info and timeslot)
        self.activity1 = activity(id="SLA100A", room="Room1", time=10, facilitator="John")
        self.activity2 = activity(id="SLA100B", room="Room2", time=11, facilitator="Claire")
        self.activity3 = activity(id="SLA191A", room="Room3", time=12, facilitator="Jorgon")
        self.activity4 = activity(id="SLA191B", room="Room1", time=13, facilitator="Claire")
        self.activity5 = activity(id="CS441", room="Room4", time=10, facilitator="Hare")
        self.activity6 = activity(id="CS353", room="Room4", time=10, facilitator="Hare")
        self.activity7 = activity(id="CS1000", room="Room4", time=10, facilitator="Tyler")

    def test_same_room_and_time_fitness(self): 
        acs = [self.activity1, self.activity2, self.activity3, self.activity4]
        result = activity.same_room_and_time_fitness(acs)
        
        # no activities should overlap in the same time/room in the
        # default test dataset
        self.assertEqual(result, 0.0)  # no fitness should be deducted

        # by adding a duplicate activity, this is no longer the case
        acs.append(self.activity1)
        result = activity.same_room_and_time_fitness(acs)
        self.assertEqual(result, -1.0)  # 0.5 fitness should be deducted for each overlapping activity

    def test_room_size_fitness(self):
        # exceeds room capacity        (-0.5)
        result1 = activity.room_size_fitness(self.activity5, self.ac_dict, self.room_dict)
        # exactly room capacity        (+0.3)
        result2 = activity.room_size_fitness(self.activity2, self.ac_dict, self.room_dict)
        # room is several times as big (-0.4)
        result3 = activity.room_size_fitness(self.activity3, self.ac_dict, self.room_dict)

        # assert
        self.assertEqual(result1, -0.5)
        self.assertEqual(result2, 0.3)
        self.assertEqual(result3, -0.4)



    def test_preferred_facilitator_fitness(self):
        # result1 has a preferred facilitator   (+0.5)
        result1 = activity.preferred_facilitator_fitness(self.activity1, self.ac_dict)
        # result2 has an "other" facilitator    (+0.2)
        result2 = activity.preferred_facilitator_fitness(self.activity2, self.ac_dict)
        # resulte3 has an unlisted facilitator  (-0.1)
        result3 = activity.preferred_facilitator_fitness(self.activity3, self.ac_dict)

        # assert
        self.assertEqual(result1, 0.5)
        self.assertEqual(result2, 0.2)
        self.assertEqual(result3, -0.1)

    def test_facilitator_load_timeslot_fitness(self):
        
        acs = [self.activity1]
        # should be (+0.2) a single activity (no conflicts)
        result1 = activity.facilitator_load_timeslot_fitness(acs)

        acs.append(self.activity2)
        # should be (+0.4) two unconflicting activities
        result2 = activity.facilitator_load_timeslot_fitness(acs)

        acs.append(self.activity5)
        acs.append(self.activity6)
        # should be (0.2) now two activities w/ same timeslot and facilitator
        result3 = activity.facilitator_load_timeslot_fitness(acs)

        self.assertEqual(result1, 0.2)
        self.assertEqual(result2, 0.4)
        self.assertEqual(result3, 0.2)


    def test_facilitator_load_num_oversee_fitness(self):
        acs = [self.activity7]
        # Tyler is the instructor, so no penalty for not enough assigned activities (+0.0)
        result1 = activity.facilitator_load_num_oversee_fitness(acs)
        self.assertEqual(result1, 0.0)

        # Hare is only overseeing one actvities so there is a penalty (-0.4)
        acs.append(self.activity5)
        result2 = activity.facilitator_load_num_oversee_fitness(acs)
        self.assertEqual(result2, -0.4)

        # Hare is only overseeing two activities so there is a penalty (-0.4)
        acs.append(self.activity5)
        result3 = activity.facilitator_load_num_oversee_fitness(acs)
        self.assertEqual(result3, -0.4)

        # Hare is overseeing an appropriate amount of activities so no penalty (0.0)
        acs.append(self.activity5)
        result4 = activity.facilitator_load_num_oversee_fitness(acs)
        self.assertEqual(result4, 0.0)
        
        # Hare is overseeing >4 activies now so there is a penalty (-0.5)
        acs.append(self.activity5)
        acs.append(self.activity5)
        result5 = activity.facilitator_load_num_oversee_fitness(acs)
        self.assertEqual(result5, -0.5)


    def test_facilitator_load_consecutive_oversee(self):
        # Claire has activities at time 10 and 11
        ac1 = activity(id="SLA100A", room="Room1", time=10, facilitator="Claire")
        ac2 = activity(id="SLA191A", room="Room2", time=11, facilitator="Claire")
        
        acs = [ac1, ac2]
        result = activity.facilitator_load_consecutive_oversee(acs)
        self.assertEqual(result, -0.5)

        # No consecutive for Bob
        ac3 = activity(id="SLA100B", room="Room1", time=9, facilitator="Bob")
        ac4 = activity(id="CS441", room="Room2", time=11, facilitator="Bob")
        acs = [ac3, ac4]
        result = activity.facilitator_load_consecutive_oversee(acs)
        self.assertEqual(result, 0.0)


    def test_activity_specific_fitness(self):
        acs = [self.activity1, self.activity2, self.activity3, self.activity4]
    
        # SLA100A - Room1, time=10
        # SLA100B - Room2, time=11 → diff = 1 (not > 4), not coincident → no +/- 0.5
        # SLA191A - Room3, time=12
        # SLA191B - Room1, time=13 → diff = 1 (not > 4), not coincident → no +/- 0.5
        # SLA100B vs SLA191A → 11, 12 → consecutive → -0.4 (not roman/beach)
        # SLA100A vs SLA191A → 10, 12 → not consecutive → no penalty/bonus

        result = activity.activity_specific_fitness(acs)
        self.assertAlmostEqual(result, -0.4 + 0.25, places=2)  # Includes the +0.25 from being consecutive

if __name__ == "__main__":
    unittest.main()