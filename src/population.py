from schedule import schedule
import heapq, random

class population:
    def __init__(self):
        # priority queue for schedules based on fitness
        self.schedules: tuple[float, schedule] = [] 


    # priority queue manipulation functions
    def _add_schedule(self, schedule_to_add:schedule):
        heapq.heappush(self.schedules, (schedule_to_add.fitness, schedule_to_add))
    def _remove_least_fit(self): heapq.heappop(self.schedules)


    def generate_schedules(self, amount: int):
        for i in range(amount):
            schedule_to_add = schedule()
            self._add_schedule(schedule_to_add)

    
    def cull_unfit(self, cull_rate: float):
        pop_size = len(self.schedules)
        num_to_cull = int(pop_size * cull_rate)
        for i in range(num_to_cull):
            self._remove_least_fit()

    
    def repopulate(self, original_pop_size: int, top_performers: list[schedule]):
        vacancies = original_pop_size - len(self.schedules)

        if vacancies == 0: return

        for i in range(vacancies):
            parent1 = random.choice(top_performers)
            parent2 = random.choice([schdl for schdl in top_performers if schdl is not parent1])
            child = self.crossover(parent1, parent2)
            self._add_schedule(child)


    def crossover(self, p1: schedule, p2: schedule) -> schedule:
        child = schedule()
        num_activities = len(p1.activities)

        for i in range(num_activities):
            child.activities[i] = random.choice([p1.activities[i], p2.activities[i]])
        
        # recalculate fitness
        child.calculate_fitness()

        return child
    

    def try_mutation(self, mutation_rate: float):
        for _, sched in self.schedules:
            if random.random() < mutation_rate:
                self._mutate(sched)
    

    def _mutate(self, sched:schedule):
        num_activities = len(sched.activities)
        mut_activity_index = random.randint(0, num_activities-1)
        activity_to_mutate = sched.activities[mut_activity_index]
        mutated_activity = schedule.generate_activity(activity_to_mutate.id)
        
        # apply the mutation
        sched.activities[mut_activity_index] = mutated_activity


    def get_top_performers(self, breeding_percentile: float) -> list[schedule]:
        pop_size = len(self.schedules)
        amount = int((1.0 - breeding_percentile) * pop_size)
        schedules_copy = [sched for _, sched in self.schedules]
        schedules_copy.sort(key=lambda sched: sched.fitness, reverse=True)
        return schedules_copy[:amount]

        


    


        


