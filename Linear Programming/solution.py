import os
import sys
import numpy as np
import cvxpy as cp
import json

x = 11 # Team Number

ENEMY_STATES = 5
ARROW_STATES = 4
STAMINA_STATES = 3

GAMMA = 0.99

arr = [0.5, 1, 2]
y = arr[x % 3]
penalty = -10 / y
shoot_penalty = -1

states = []

actions = [0, 1, 2] #Shoot, Dodge, Recharge

INT_MIN = -10e9

map = []

def check_valid(state):
    
    if state[0] < 0 or state[1] < 0 or state[2] < 0:
        return False
    if state[0] > 5 or state[1] > 3 or state[2] > 2:
        return False
    
    return True

def set_up_states():
    
    for i in range(ENEMY_STATES):
        for j in range(ARROW_STATES):
            for k in range(STAMINA_STATES):
                states.append( [i, j, k] )
                
def print_states():

    for i in range(len(states)):
        print(states[i])

def get_index(state):

    for i in range(len(states)):
        if str(state) == str(states[i]):
            return i

def create_matrix():

    A = []
      
    for i in range(len(states)):

        if states[i][0] == 0:

            array = []

            for k in range(len(states)):
                array.append(0)
            
            array[get_index(states[i])] = 0
            A.append(array)
            
            map.append({
                "state": states[i],
                "action": "NOOP",
            })

            continue

        for j in range(len(actions)):
            
            array = []

            for k in range(len(states)):
                array.append(0)

            curr_state = states[i][:]
                    
            # SHOOT
            if j == 0:

                # Reduce arrow count and stamina
                curr_state[1] -= 1
                curr_state[2] -= 1

                # If reducing isn't possible, don't do it            
                if not check_valid(curr_state):
                    curr_state[1] += 1
                    curr_state[2] += 1
                    continue

                probabilities = [0.5, 0.5]
                array[get_index(curr_state)] += 0.5
                array[get_index([curr_state[0] - 1, curr_state[1], curr_state[2]])] += 0.5

                map.append({
                    "state": states[i],
                    "action": "SHOOT",
                })

            # DODGE
            elif j == 1:

                # If stamina is 50
                if curr_state[2] == 1:

                    curr_state[2] = 0
                    probabilities = [0.2, 0.8]
                    array[get_index(curr_state)] += 0.2
                    array[get_index([curr_state[0], 3 if (curr_state[1] + 1) >= 3 else (curr_state[1] + 1), 
                                                        curr_state[2]])] += 0.8

                    map.append({
                        "state": states[i],
                        "action": "DODGE",
                    })                    

                # If stamina is 100
                elif curr_state[2] == 2:

                    # 50 stamina reduction, pickup / not pickup , 100 stamina reduction, pickup/not pickup
                    probabilities = [0.64, 0.16, 0.16, 0.04]
                    array[get_index([curr_state[0], 3 if (curr_state[1] + 1) >= 3 
                                                    else (curr_state[1] + 1), curr_state[2] - 1])] += 0.64
                    array[get_index([curr_state[0], curr_state[1], curr_state[2] - 1])] += 0.16
                    array[get_index([curr_state[0], 3 if (curr_state[1] + 1) >= 3 
                                                    else (curr_state[1] + 1), curr_state[2] - 2])] += 0.16
                    array[get_index([curr_state[0], curr_state[1], curr_state[2] - 2])] += 0.04


                    map.append({
                        "state": states[i],
                        "action": "DODGE",
                    })
                else:
                    continue

            # RECHARGE
            elif j == 2:

                probabilities = [0.2, 0.8]

                if (curr_state[2] + 1) > 2:
                    continue
 
                array[get_index([curr_state[0], curr_state[1], 2 if (curr_state[2] + 1) >= 2 else 
                                                (curr_state[2] + 1)])] += 0.8
                array[get_index(curr_state)] += 0.2
                map.append({
                    "state": states[i],
                    "action": "RECHARGE",
                })
            
            A.append(array)
    
    return A

def return_A_matrix():
    A = np.array(create_matrix())
    A = A.transpose()

    for i in range(A.shape[0]):
        for j in range(A.shape[1]):

            assert A[i][j] >= 0

            A[i][j] *= -1

            if str(states[i]) == str(map[j]["state"]):
                A[i][j] += 1

    return A

def return_r_vector():
    r = []
    for i in range(100):
        if map[i]["state"][0] != 0:
            r.append(penalty)
        else:
            r.append(0)
    return np.array(r)

def return_alpha_vector():
    alpha = [0] * len(states)
    alpha[get_index([4, 3, 2])] = 1
    return np.array(alpha).reshape(len(states),1)

def write_to_file(A, r, alpha, x, policy, solution):

    alpha = alpha.reshape(1, len(states))[0]

    data = {
        "a": A.tolist(),
        "r": r.tolist(),
        "alpha": alpha.tolist(),
        "policy": policy,
        "objective": solution,
        "x": x,
    }

    if not os.path.exists("outputs"):
        os.mkdir("outputs")

    with open("outputs/output.json", "w") as f:
        json.dump(data, f, indent=5)

def find_policy(x):

    new_x = []

    for i in range(len(x.value)):
        new_x.append(x.value[i][0])

    i = 0
    max = i

    policy = []

    while i < len(new_x):

        state = map[i]["state"]
        max = i
        # print(state)

        while i < len(new_x) and str(map[i]["state"]) == str(state):
            
            if new_x[i] > new_x[max]:
                max = i
            
            i += 1

        policy.append([state, map[max]["action"]])

    return policy, new_x

def solve(A, x, r, alpha):

    constraints = [cp.matmul(A, x) == alpha, x>=0]
    objective = cp.Maximize(cp.sum(cp.matmul(r,x), axis=0))
    problem = cp.Problem(objective, constraints)

    solution = problem.solve()
    print(solution)
    
    policy, x = find_policy(x)

    write_to_file(A, r, alpha, x, policy, solution)

def main():
    set_up_states()
    
    A = return_A_matrix()
    x = cp.Variable(shape=(A.shape[1], 1), name="x")
    r = return_r_vector()
    alpha = return_alpha_vector()

    solve(A, x, r, alpha)

if __name__=='__main__':
    main()