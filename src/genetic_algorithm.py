from data import config
from schedule import schedule
from population import population

class genetic_algorithm:
    def __init__(self):
        self.is_first_generation = True
        self.population_size = config["population_size"]             # the size of each generation

        self.min_num_generations = config["min_num_of_generations"]  # the minumum number of generations the algorithm will run
        
        self.improvement_cutoff = config["improvement_delta_cutoff"] # if inter-gen fitness % improvement is below this after <min_num_generations>
                                                                     # threshold has been reached, stop the algorithm

        self.mutation_rate = config["mutation_rate"]                 # the % chance that a member of the population will be selected for mutation
                                                                     # in each generation

        self.cull_percentage = config["cull_percentage"]             # the bottom <cull_percentage> of performers will be removed

        self.breeding_percentile = config["breeding_percentile"]     # members at/above this percentile of fitness will breed to replace the culled
                                                                     # members

        # current population
        self.current_pop = population()
    

    def is_sufficient_improvement(self, current_avg, prev_avg) -> bool:

        if prev_avg > current_avg: return False                   # fitness avg decreased: return False
        elif prev_avg == 0.0 and current_avg != 0.0: return True  # fitness avg increased from 0 to some other value: return True
        else:
            delta = current_avg - prev_avg
            percentage_improvement = delta / prev_avg
            return percentage_improvement > self.improvement_cutoff


    def run(self, log_file, output_file) -> None:
        
        # initialization logic
        # --------------------
        self.current_pop.generate_schedules(self.population_size)  # generate population
        current_avg_fitness = self.current_pop.get_fitness_avg()   # calculate the avg fitness of population
        prev_avg_fitness = 0.0                                     # initilize the prev avg fitness to 0.0
        generation_counter = 0                                     # counter for how many generations have passed


        # genetic algorithm
        # -----------------
        while (generation_counter < self.min_num_generations 
               or self.is_sufficient_improvement(current_avg_fitness, prev_avg_fitness)):
            
            self.current_pop.cull_unfit(self.cull_percentage)                              # cull the least fit
            top_performers = self.current_pop.get_top_performers(self.breeding_percentile) # get the top performers
            self.current_pop.repopulate(self.population_size, top_performers)              # repopulate by breeding top performers
            self.current_pop.try_mutation(self.mutation_rate)                              # apply mutation

            # update state before looping
            # ---------------------------
            prev_avg_fitness = current_avg_fitness
            current_avg_fitness = self.current_pop.get_fitness_avg()
            generation_counter += 1

            # update log file
            # ---------------
            log_file.write(f'\n---\nGEN #{generation_counter}\nAVG FITNESS: {round(prev_avg_fitness, 3)}')

        
        # post-algorithm
        # --------------
        best_schedule = self.current_pop.get_top_performers(self.breeding_percentile)[0]
        string_representation = str(best_schedule)
        output_file.write(f'BEST SCHEDULE:\n- - - - - - - - -\n - - - - - - - -\n')
        output_file.write(f'{string_representation}')
        output_file.write(f'\n*********************************\n')
        output_file.write(f'FITNESS: {best_schedule.fitness}')
