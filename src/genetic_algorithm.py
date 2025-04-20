from data import config
from population import population

class genetic_algorithm:
    def __init__(self):
        self.is_first_generation = True
        self.population_size = config["population_size"]
        self.min_num_generations = config["min_num_of_generations"]
        self.improvement_cutoff = config["improvement_delta_cutoff"]
        self.mutation_rate = config["mutation_rate"]

