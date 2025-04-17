import csv
from pathlib import Path

room_path = Path(__file__).resolve().parent.parent / 'data' / 'rooms.csv'
activities_path = Path(__file__).resolve().parent.parent / 'data' / 'activities.csv'


# activity into class for storing predefined activity information from activities.csv
class activity_info:
    def __init__(self, expected_enrollment, preferred_facilitators, other_facilitators):
        self.expected_enrollment = expected_enrollment
        self.preferred_facilitators = preferred_facilitators
        self.facilitators = other_facilitators


# function for getting all activities
def get_activities() -> dict:
    out = dict()

    with open(activities_path, mode="r", newline="") as activities_file:
        reader = csv.reader(activities_file)
        next(reader)

        for row in reader:
            new_activity = activity_info(
                int(row[1]),         # the expected enrollment
                set(row[2].split()), # the set of preferred facilitators
                set(row[3].split())  # the set of other facilitators
            )
            out[row[0]] = new_activity
    return out

    
# function for getting all rooms
def get_rooms() -> dict:
    out = dict()

    with open(room_path, mode="r", newline="") as rooms_file:
        reader = csv.reader(rooms_file)
        next(reader)

        for row in reader:
            room_name = row[0]
            capacity = int(row[1])
            out[room_name] = capacity
    return out


rooms = get_rooms()            # dict that maps room_name to capacity
activities = get_activities()  # dict that maps activity_name to instance of activity_info
facilitators = {'Lock', 'Glen', 'Banks', 'Richards', 'Shaw', 'Singer', 'Uther', 'Tyler', 'Numen', 'Zeldin'}
times = [10, 11, 12, 1, 2, 3]