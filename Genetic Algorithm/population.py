import numpy as np
from genetic import avg
from colorama import Fore

class Population:

    def __init__(self, pop=False):

        if pop:
            self.population = np.array(pop)
        else:
            self.population = []

    def add_individual(self, individual):
        pass

    def append(self, individual):
        self.population.append(individual)

    def sort(self):
        modified_fitness = []

        for i in range(len(self.population)):
            if abs(self.population[i].fitness[0] - self.population[i].fitness[1]) > 300000:
                modified_fitness.append(avg(self.population[i].fitness) + 200000)
            else:
                modified_fitness.append(avg(self.population[i].fitness))

        for i in range(len(self.population)):
            for j in range(0, len(self.population) - i - 1):
                if modified_fitness[j] > modified_fitness[j+1] :
                    self.population[j], self.population[j+1] = self.population[j+1], self.population[j]
        
    def size(self):
        return len(self.population)

    def get_fittest(self):
        
        self.sort()
        best = self.population[0]

        return best

    def __str__(self):
        out = Fore.YELLOW
        pop = []
        for i in range(len(self.population)):
            pop.append([list(self.population[i].vector), avg(self.population[i].fitness)])
            out += (str(i) + str([list(self.population[i].vector), avg(self.population[i].fitness)]) + "\n")
        out += ("\n" + Fore.RESET)
        return out

    def __len__(self):
        return len(self.population)