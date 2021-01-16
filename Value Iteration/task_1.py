import os
import sys

orig_stdout = sys.stdout

x = 87 # Team Number

ENEMY_STATES = 5
ARROW_STATES = 4
STAMINA_STATES = 3

GAMMA = 0.99
DELTA = 0.001

arr = [0.5, 1, 2]
y = arr[x % 3]
penalty = -10/y
shoot_penalty = -1

states = []
utilities = [{}]

actions = [0, 1, 2] # Shoot, Dodge, Recharge

INT_MIN = -10e9

def check_valid(state):
    
    if state[0] < 0 or state[1] < 0 or state[2] < 0:
        return False
    if state[0] > 5 or state[1] > 3 or state[2] > 2:
        return False
    
    return True

"""
This function calculates the utility of the state for time t+1 when
given the utility at time t

@params {
    state = an object with probability of distribution of proceeding
            to another state
    time = the previous time of the 
}
"""

def next_util(new_state, time):

    best_utility = INT_MIN
    action = ""
    
    for action_count in range(3):
        curr_state = new_state[:]
        new_util = 0
                
        # SHOOT
        if action_count == 0:

            # Reduce arrow count and stamina
            curr_state[1] -= 1
            curr_state[2] -= 1

            # If reducing isn't possible, don't do it            
            if not check_valid(curr_state):
                curr_state[1] += 1
                curr_state[2] += 1
                continue

            probabilities = [0.5, 0.5]
            old_util = [utilities[time][str(curr_state)], utilities[time][str([curr_state[0] - 1, curr_state[1], curr_state[2]])]]

            step = []
            
            if shoot_penalty < 0:
                step = [penalty] * 2
            else:
                step = [shoot_penalty] * 2

            # If dragon has only one life left, the reward is not just penalty, it includes
            # the reward of +10 as this is a terminal state
            if curr_state[0] == 1:
                step[1] += 10

            # This is calculated as probability *( reward + gamma * utility)
            for i in range(2):
                new_util += probabilities[i]*(step[i] + GAMMA*old_util[i])

            if best_utility < new_util:
                action = "SHOOT"

            best_utility = max(best_utility, new_util)

        # DODGE
        elif action_count == 1:

            # If stamina is 50
            if curr_state[2] == 1:

                curr_state[2] = 0
                probabilities = [0.2, 0.8]
                old_util = [utilities[time][str(curr_state)], 
                            utilities[time][str([curr_state[0], 3 if (curr_state[1] + 1) >= 3 else (curr_state[1] + 1), 
                                                    curr_state[2]])]]

                step = [penalty] * 2

                # This is calculated as reward + probability * utility
                for i in range(2):
                    new_util += probabilities[i]*(step[i] + GAMMA*old_util[i])
                    
                if best_utility < new_util:
                    action = "DODGE"
                best_utility = max(best_utility, new_util)

            # If stamina is 100
            elif curr_state[2] == 2:

                # 50 stamina reduction, pickup / not pickup , 100 stamina reduction, pickup/not pickup
                probabilities = [0.64, 0.16, 0.16, 0.04]
                old_util = [utilities[time][str([curr_state[0], 3 if (curr_state[1] + 1) >= 3 
                                                 else (curr_state[1] + 1), curr_state[2] - 1])]
                            , utilities[time][str([curr_state[0], curr_state[1], curr_state[2] - 1])]
                            , utilities[time][str([curr_state[0], 3 if (curr_state[1] + 1) >= 3 
                                                   else (curr_state[1] + 1), curr_state[2] - 2])]
                            , utilities[time][str([curr_state[0], curr_state[1], curr_state[2] - 1])]
                           ]

                step = [penalty] * 4

                # This is calculated as reward + probability * utility
                for i in range(4):
                    new_util += probabilities[i]*(step[i] + GAMMA*old_util[i])

                if best_utility < new_util:
                    action = "DODGE"
                best_utility = max(best_utility, new_util)

        # RECHARGE
        elif action_count == 2:

            probabilities = [0.2, 0.8]
            old_util = [utilities[time][str(curr_state)], 
                        utilities[time][str([curr_state[0], 
                                             curr_state[1], 2 if (curr_state[2] + 1) >= 2 else 
                                             (curr_state[2] + 1)])]]

            step = [penalty] * 2

            # This is calculated as reward + probability * utility
            for i in range(2):
                new_util += probabilities[i]*(step[i] + GAMMA*old_util[i])

            if best_utility < new_util:
                action = "RECHARGE"
            best_utility = max(best_utility, new_util)

    return best_utility, action
    
"""
This function sets up the states and initializes all states with the corresponding utility
values
"""
def set_up_states():
    
    for i in range(ENEMY_STATES):
        for j in range(ARROW_STATES):
            for k in range(STAMINA_STATES):
                states.append( [i, j, k] )
                utilities[0][str( [i, j, k] )] = 0

def print_output(state, action, utility):
    print("(", end='')
    for i in range(3):
        print(state[i], end='')
        if i != 2:
            print(",", end='')
    print(")", end='')
    print(":" + str(action), end='')
    print("=[", end='')
    print(str(utility) + "]")
                
def value_iteration(file_ptr):
    
    sys.stdout = file_ptr
    
    # Each iteration will be considered to be at time t
    time = 0
    while True:
        
        print("iteration=" + str(time))
        
        util_diff = INT_MIN
        utilities.append({})
        
        for state in states:
            if state[0] == 0:
                utilities[time + 1][str(state)] = 0
                print_output(state, -1, 0)
                continue
            
            util_next, action = next_util(state[:], time)
            print_output(state, action, round(util_next, 3))
            utilities[time + 1][str(state)] = util_next
            util_diff = max(util_diff, abs(util_next - utilities[time][str(state)]))
                   
        if util_diff < DELTA:
            break

        # Append a new utility list for the time t+1
        time += 1
        
    sys.stdout = orig_stdout

def task_1():
    f = open("./outputs/task_1_trace.txt", "w")
    value_iteration(f)
    f.close() 
    
def task_2_part_1():
    global shoot_penalty 
    shoot_penalty = -0.25
    f = open("./outputs/task_2_part_1_trace.txt", "w")
    value_iteration(f)
    f.close()
    shoot_penalty = -1
    
def task_2_part_2():
    global GAMMA 
    GAMMA = 0.1
    f = open("./outputs/task_2_part_2_trace.txt", "w")
    value_iteration(f)
    f.close() 

def task_2_part_3():
    global DELTA 
    DELTA = 1e-10
    f = open("./outputs/task_2_part_3_trace.txt", "w")
    value_iteration(f)
    f.close()
    
def task_2():
    global penalty 
    penalty = -2.5
    task_2_part_1()
    task_2_part_2()
    task_2_part_3()

def create_output_folder(path):
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)        
    
def main():
    set_up_states()
    create_output_folder('./outputs')
    task_1()
    task_2()
    
if __name__=='__main__':
    main()