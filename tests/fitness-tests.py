import sys
sys.path.append('src')

import unittest
from activity import activity
from data import activity_info

class TestActivity(unittest.TestCase):

    def setUp(self):
        # Initialize common test data
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

        # Room capacities (example)
        self.room_dict = {
            "Room1": 30,   # Room1 can hold 30 people
            "Room2": 50,   # Room2 can hold 50 people
            "Room3": 1000, # Big Room
            "Room4": 5     # Tiny room
        }

        # Activities (with facilitator info and timeslot)
        self.activity1 = activity(id="SLA100A", room="Room1", time=10, facilitator="John")
        self.activity2 = activity(id="SLA100B", room="Room2", time=11, facilitator="Alice")
        self.activity3 = activity(id="SLA191A", room="Room3", time=12, facilitator="Bob")
        self.activity4 = activity(id="SLA191B", room="Room1", time=13, facilitator="Claire")
        self.activity5 = activity(id="CS441", room="Room4", time=10, facilitator="Hare")

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

        self.assertEqual(result1, -0.5)
        self.assertEqual(result2, 0.3)
        self.assertEqual(result3, -0.4)



    def test_preferred_facilitator_fitness(self):
        pass

    def test_facilitator_load_timeslot_fitness(self):
        pass


    def test_facilitator_load_num_oversee_fitness(self):
        pass

    def test_facilitator_load_consecutive_oversee(self):
        pass

    def test_activity_specific_fitness(self):
        pass

if __name__ == "__main__":
    unittest.main()