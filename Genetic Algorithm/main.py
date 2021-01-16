from local_settings import KEY, OVERFIT
from population import *
from individual import *
from random import randint,random
from colorama import Fore, Style, Back
from client_moodle import submit

import numpy as np
import pickle

NC = 2

def save_last_trace(population):
    with open("last_trace.data", "wb") as fp:
        new_list = []
        for i in range(len(population)):
            new_list.append([list(population.population[i].vector), avg(population.population[i].fitness)])
        pickle.dump(new_list, fp)

def save_population(population_list):
    with open("all_individuals.data", "wb") as fp:
        pickle.dump(population_list, fp)

def reproduce(first_parent, second_parent):

    assert len(first_parent) == 11
    assert len(second_parent) == 11
    
    child1 = Individual()
    child2 = Individual()

    eta = 20

    for i in range(11):
        
        rand = random()

        beta = 1

        if rand > 0.5:
            beta = (1 / (2. *(1 - rand)))
        else:
            beta = (2. * rand)
        
        beta **= (1. / (eta + 1.))

        child1.vector = np.append(child1.vector, 0.5 * (((1 + beta) * first_parent.vector[i]) + ((1 - beta) * second_parent.vector[i])))
        child2.vector = np.append(child2.vector, 0.5 * (((1 + beta) * second_parent.vector[i]) + ((1 - beta) * first_parent.vector[i])))

        if child1.vector[i] > 10 or child1.vector[i] < -10:
            child1.vector = first_parent.vector[i]

        if child2.vector[i] > 10 or child2.vector[i] < -10:
            child2.vector = second_parent.vector[i]

    # rand1 = randint(0,9)
    # rand2 = randint(rand1+1,10)

    # temp1 = []
    # temp2 = []

    # for i in range(0,rand1):
    #     temp1.append(first_parent.vector[i])
    #     temp2.append(second_parent.vector[i])

    # for i in range(rand1,rand2):
    #     temp1.append(second_parent.vector[i])
    #     temp2.append(first_parent.vector[i])

    # for i in range(rand2,11):
    #     temp1.append(first_parent.vector[i])
    #     temp2.append(second_parent.vector[i])

    # child1.vector = np.array(temp1)
    # child2.vector = np.array(temp2)

    # rand = randint(1, 9)

    # for i in range(len(first_parent)):
    #     if i > rand:
    #         child1.vector = np.append(child1.vector, first_parent.vector[i])
    #         child2.vector = np.append(child2.vector, second_parent.vector[i])
    #     else:
    #         child2.vector = np.append(child2.vector, first_parent.vector[i])
    #         child1.vector = np.append(child1.vector, second_parent.vector[i])

    # assert len(child1) == 11
    # assert len(child2) == 11
        
    return [child1, child2]

def populate(population):

    new_population = Population()

    for i in range(int(len(population) / 10)):
        temp = population.population[i]
        # temp = temp.mutate()
        new_population.population = np.append(new_population.population, temp)

    for i in range(int(len(population) / 10), len(population), 2):

        rand1 = randint(0,  int( (2 * len(population)) / 3))      #Pick random from top
        rand2 = randint(0, int( (2 * len(population)) / 3 ))      #Pick random from top

        first_parent = population.population[rand1]
        second_parent = population.population[rand2]

        child = reproduce(first_parent, second_parent)

        child[0] = child[0].mutate()
        child[1] = child[1].mutate()

        new_population.population = np.append(new_population.population, child[0])
        new_population.population = np.append(new_population.population, child[1])

    new_population.sort()

    return new_population

def avg(list):
    return (list[0] + list[1])/2

def genetic_algorithm(population):

    i = 0
    population_list = []
    while True and i < 100:

        i = i + 1

        fittest = population.get_fittest()
        submit(KEY, list(fittest.vector))
        print(i, Fore.RED + str(len(population)) + Fore.RESET, list(fittest.vector), Fore.GREEN + str(avg(fittest.fitness)) + Fore.RESET, fittest.fitness)
        print("---------------")
        
        if avg(fittest.fitness) <= 1e4:
            save_last_trace(population)
            save_population(population_list)
            print("ENDED")
            break

        population.sort()

        new_population = populate(population)

        for j in range(len(population)):
            population_list.append([list(population.population[j].vector), avg(population.population[j].fitness) ])

        population = new_population
        
        if i%5 == 0:
            print(population)

        save_last_trace(population)

    fittest = population.get_fittest()
    submit(KEY, list(fittest.vector))
    print(i, Fore.RED + str(len(population)) + Fore.RESET, list(fittest.vector), Fore.GREEN + str(avg(fittest.fitness)) + Fore.RESET, fittest.fitness)
    print("---------------")

    save_population(population_list)

def first_init():
    pop = []

    for i in range(10):
        person = Individual(OVERFIT, False, False)
        person = person.mutate(0)
        pop.append(person)

    for i in range(5):
        person = Individual(OVERFIT, False, False)
        person = person.mutate(0, 2)
        pop.append(person)

    # pop.append(Individual(BEST))

    for i in range(2):
        person = Individual(BEST, False, False)
        person = person.mutate(0)
        pop.append(person)

    for i in range(0):
        person = Individual(BEST, False, False)
        person = person.mutate(0, 2)
        pop.append(person)

    # with open("last_trace.data", "rb") as fp:
    #     data = pickle.load(fp)
    #     data = sort_all(data)

    #     for i in range(4):
    #         pop.append(Individual(data[i][0]))

    # for i in range(4):
    #     person = Individual([-4.953649279947332e-14, 0.12119706586017825, -6.445067263467308, 0.08425235331447335, 0.03846886029743811, 8.118911173407719e-05, -6.0187691609169116e-05, -1.313443631190975e-07, 3.484096383229681e-08, 3.997491889644974e-11, -6.732420176902564e-12], 
    #         False, False)
    #     person = person.mutate(0, 2)
    #     pop.append(person)

    # for i in range(2):
    #     person = Individual([-2.969319343154344e-11, 1.8715420139593866, -6.922088493160181, 0.06539782444542824, 0.03870620199603078, 9.28803139883789e-05, -6.01876914689282e-05, -1.2957851278314178e-07, 3.484096383229683e-08, 3.825538145448347e-11, -6.732420176902685e-12]
    #     , False, False)
    #     person = person.mutate(0)
    #     pop.append(person)

    return pop

def sort_all(data):

    for i in range(len(data)):
        for j in range(0, len(data) - i - 1):
            if data[j][1] > data[j+1][1] :
                data[j], data[j+1] = data[j+1], data[j]
    return data

def read_load():
    pop = []
    with open("all_individuals.data", "rb") as fp:
        data = pickle.load(fp)
        data = sort_all(data)

        for i in range(10):
            pop.append(Individual(data[i][0]))

    return pop

def load_last():

    pop = []

    with open("last_trace.data", "rb") as fp:
        data = pickle.load(fp)

        # pop.append(Individual(data[0][0]))

        for i in range(6):

            person = Individual(data[i][0])
            # person = person.mutate(0)

            # if i == 0:
            #     while avg(person.fitness) <= 900000 or avg(person.fitness) > 1300000:
            #         print("Stuck")
            #         person = person.mutate(0)
            # else:
            #     i
            #     while avg(person.fitness) > 2500000:
            #         person = person.mutate(0)

            pop.append(person)
            
    #         if i < 3:
    #             pop.append(person.mutate(0))

    for i in range(6):
        person = Individual(OVERFIT, False, False)
        person = person.mutate(0)
        pop.append(person)

    return pop

def load_overfit_mutated():
    pop = []
    template = Individual(BEST)
    pop.append(template)

    best_count = 0

    for i in range(best_count):
        person = template
        person = person.mutate(0.85, 1)
        pop.append(person)

    template = Individual(OVERFIT)
    pop.append(template)

    overfit_count = 0

    for i in range(overfit_count):
        person = template
        person = person.mutate(0.85, 2)
        pop.append(person)

    for i in range(10):
        pop.append(Individual(OVERFIT))
        pop.append(Individual(BEST))

    return pop

def init_pop(option=3):
    if option == 1:
        return first_init()
    elif option == 2:
        return read_load()
    elif option == 3:
        return load_last()
    else:
        return load_overfit_mutated()

if __name__ == '__main__':

    population = init_pop(3)
    population = Population(population)
    print(population)
    genetic_algorithm(population)