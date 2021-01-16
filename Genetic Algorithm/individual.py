import numpy as np
from random import randint, random
from client_moodle import get_errors
from local_settings import *

class Individual:

    def __init__(self, vector=False, is_random=False, calcFitness=True):
        
        if is_random:

            vector = OVERFIT

        if isinstance(vector, np.ndarray):

            self.vector = np.copy(vector)

            if calcFitness:
                # pass
                self.fitness = get_errors(KEY, list(self.vector))
                # print(list(self.vector), self.fitness, (self.fitness[0] + self.fitness[1])/2)
            # print(self.fitness)

        elif isinstance(vector, list):

            # power = [0, 0, 0, 0, 0, 4, 4, 6, 7, 10, 11]

            self.vector = np.array(vector)
            # for i in range(len(self.vector)):
            #     rand = np.random.random()
            #     self.vector[i] += (self.vector[i] * rand)
            
            if calcFitness:
                # pass
                self.fitness = get_errors(KEY, list(self.vector))
                # print(list(self.vector), self.fitness, (self.fitness[0] + self.fitness[1])/2)
            # print(self.fitness)

        else:

            self.vector = np.array([])
            self.fitness = [-1, -1]

    def mutate(self, prob=0.7, count=1):

        tempInd = np.copy(self.vector)
        for i in range(count):
            if random() > prob:

                rand = randint(0, 10)

                if -1 < tempInd[rand] < 1:
                    tempInd[rand] += (tempInd[rand] * np.random.uniform(-0.5, 0.5))
                else:
                    while True:
                        val = tempInd[rand] * np.random.uniform(-0.25, 0.25)
                        val += tempInd[rand]

                        if -10 <= val <= 10:
                            tempInd[rand] = val
                            break

                assert -10 <= tempInd[rand] <=10 


        return Individual(list(tempInd))

    def calcFitness(self):
        self.fitness = get_errors(KEY, list(self.vector))

    def getFitness(self):
        return self.fitness

    def __str__(self):
        return str(list(self.vector))

    def __len__(self):
        return len(self.vector)