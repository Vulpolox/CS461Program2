from data import config
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

