from random import randint,uniform,random
import numpy as np

def reproduce(first_parent, second_parent):
    child1 = []
    child2 = []

    eta = 10

    for i in range(6):
        
        rand = random()

        beta = 1

        if rand > 0.5:
            beta = (1 / (2. *(1 - rand)))
        else:
            beta = (2. * rand)
        
        beta **= (1. / (eta + 1.))


        child1.append( 0.5 * (((1 + beta) * first_parent[i]) + ((1 - beta) * second_parent[i])))
        child2.append(0.5 * (((1 + beta) * second_parent[i]) + ((1 - beta) * first_parent[i])))

    return [child1, child2]

def mutate(child, prob=0.7, count=1):
    
    if random() > prob:
        rand = randint(0, 5)
        print("MUTATING",rand)
        print(child)

        child[rand] += child[rand]*uniform(-0.01,0.01)
        print("NEW VALUE")
        print(child)
    return child

def populate(population):

    new_population = []

    for i in range(int(len(population) / 10)):
        temp = population[i]
        new_population.append(temp)


    for i in range(int(len(population) / 10), len(population), 2):

        rand1 = randint(0,  int( (2 * len(population)) / 3))      #Pick random from top
        rand2 = randint(0, int( (2 * len(population)) / 3 ))      #Pick random from top

        first_parent = population[rand1]
        second_parent = population[rand2]


        print("THE PARENTS ARE")
        print(first_parent)
        print(second_parent)
        child = reproduce(first_parent, second_parent)
        print("THE CHILDREN ARE")
        print(child[0])
        print((child[1]))


        child0 =  mutate(child[0])
        child1 =  mutate(child[1])

        print("POST MUTATION")
        print(child0)
        print(child1)




        new_population.append(child0)
        new_population.append(child1)
    return new_population

population =    [[9.999524199128863e-18, 0.6266267501754864, -5.736704374897544, 0.04693211506829981, 0.03811383532777356, 0.00010319567475870432],
                [1.0000007369241955e-17, 0.6260461677630377, -5.742326703867255, 0.04651496164122779, 0.03811321783619889, 0.00010319618172234475],
                [9.953790076431333e-18, 0.6260257427205314, -5.7425642977106905, 0.04677760952942613, 0.03831186969978494, 0.00010319637001732787],
                [1.1674461733697191e-17, 0.6339930303884016, -5.7276223572162275, 0.046514958585270307, 0.04835853006675481, 0.00010319268809593746],
                [1.0000075034825863e-17, 0.626061571155988, -5.752413210286028, 0.046514961642754676, 0.03811328186060293, 0.00010319616101383122],
                [9.999456533544954e-18, 0.6266113467825363, -5.7377024247790915, 0.04651496146921629, 0.038113771303369515, 0.00010319569546721785],
                [9.99954866738511e-18, 0.6318363163307538, -5.73674548535132, 0.04651496224158121, 0.0381044595616381, 0.000102617222400246],
                [1.0000019475514357e-17, 0.7550934033840231, -5.744739679355673, 0.046514888730490506, 0.03819699380620194, 0.00010130497288378867]]




new_pop = populate(population)

# print((population))
# print((new_pop))