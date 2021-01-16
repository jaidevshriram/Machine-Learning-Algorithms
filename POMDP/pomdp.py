import sys

orig_stdout = sys.stdout

rollnumber = 2018101017
x = 1-((((rollnumber%1000)%40)+1)/100)
print(x)

STATES = []
ACTIONS = []
INITIAL_BELIEF = []

def check_start_dist(state):
    agent_pos = state[0]
    target_pos = state[1]

    if agent_pos in [(1, 0), (2, 1), (0, 1), (1, 2), (1, 1)]:
        return False
    return True

def is_terminal(state):

    if state[0] == state[1] and state[2] == 1:
        # print(state, file=orig_stdout)
        return True
    return False

def isvalid(state):

    if state[0] <=2 and state[0] >=0 and state[1] >= 0 and state[1] <=2:
        return True
    return False

def setup():

    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    for m in range(2):
                        STATES.append([(i, j), (k, l), m])

    for i in range(5):
        ACTIONS.append(i)

def ret_index(state):

    for i in range(len(STATES)):
        if state == STATES[i]:
            return i

    print("ERROR", state, file=orig_stdout)
    return -1

def sum_list(a):

    sum = 0
    for i in range(len(a)):
        sum += a[i]

    return sum

def init_start():
    count = 0

    for i in range(len(STATES)):
        if check_start_dist(STATES[i]) and STATES[i][1] == (1, 1):
        # if STATES[i][0] == (0, 1) and STATES[i][2] == 0 and STATES[i][1] in [(0, 0), (0, 1), (0, 2), (1, 1)]:
            count += 1

    print(count, file=orig_stdout)

    print("start:")
    for i in range(len(STATES)):
        if check_start_dist(STATES[i]) and STATES[i][1] == (1, 1):
            INITIAL_BELIEF.append(1/count)
            print(1/count, end=" ")
        else:
            INITIAL_BELIEF.append(0)
            print(0, end=" ")
    print("")

def emulate_call(old_states, old_prob):

    new_states = []
    prob = []

    for i in range(len(old_states)):
        curr_state = old_states[i]
        prob_state = old_prob[i]
        call = curr_state[2]

        # if ret_index(curr_state) == 1:
        #     print(curr_state, prob_state, file=orig_stdout)

        if call == 1:

            # if is_terminal(curr_state):
            #     new_states.append([curr_state[0], curr_state[1], 0])
            #     # if ret_index(curr_state) == 3:
            #     print("HERE", file=orig_stdout)
            #     prob.append(prob_state * 1)
            # else:
            new_states.append(curr_state)
            prob.append(prob_state * 0.8)

            new_states.append([curr_state[0], curr_state[1], 0])
            prob.append(prob_state * 0.2)

        else:       
            new_states.append(curr_state)
            prob.append(prob_state * 0.6)

            new_states.append([curr_state[0], curr_state[1], 1])
            prob.append(prob_state * 0.4)

        # if ret_index(curr_state) == 1:
        #     print(curr_state, prob_state, file=orig_stdout)
        #     print(new_states, prob, file=orig_stdout)

    assert len(new_states) == 2*len(old_states)
    assert round(sum_list(prob), 5) == round(sum_list(old_prob), 5)

    return new_states, prob

def emulate_target(old_states, old_prob):

    new_states = []
    prob = []

    for i in range(len(old_states)):

        curr_state = old_states[i]

        for j in range(len(ACTIONS)):

            prob_state = old_prob[i]
            target_pos = curr_state[1]

            if j == 0:
                curr_state = curr_state
                new_states.append(curr_state)
                prob.append(prob_state * 0.4)

            # Up
            elif j == 1:
                if isvalid((target_pos[0], target_pos[1] + 1)):
                    new_states.append([curr_state[0], (target_pos[0], target_pos[1] + 1), curr_state[2]])
                else:
                    new_states.append(curr_state)
                prob.append(prob_state * 0.15)

            # Down
            elif j == 2:
                if isvalid((target_pos[0], target_pos[1] - 1)):
                    new_states.append([curr_state[0], (target_pos[0], target_pos[1] - 1), curr_state[2]])
                else:
                    new_states.append(curr_state)
                prob.append(prob_state * 0.15)

            # Left
            elif j == 3:
                if isvalid((target_pos[0] - 1, target_pos[1])):
                    new_states.append([curr_state[0], (target_pos[0] - 1, target_pos[1]), curr_state[2]])
                else:
                    new_states.append(curr_state)
                prob.append(prob_state * 0.15)

            # Right
            elif j == 4:
                if isvalid((target_pos[0] + 1, target_pos[1])):
                    new_states.append([curr_state[0], (target_pos[0] + 1, target_pos[1]), curr_state[2]])
                else:
                    new_states.append(curr_state)
                prob.append(prob_state * 0.15)

    assert len(ACTIONS)*len(old_states) == len(new_states)

    # print(old_prob, file=orig_stdout)
    # print(prob, file=orig_stdout)
    # print(sum_list(old_prob), sum_list(prob), file=orig_stdout)

    assert round(sum_list(old_prob), 5) == round(sum_list(prob), 5)

    new_states, prob = emulate_call(new_states, prob)

    return new_states, prob

def create_transition_matrix():
    T = []

    for i in range(len(ACTIONS)):

        T_Action = []

        # Start State
        for j in range(len(STATES)):

            probabilities = [0] * len(STATES)
            curr_state = STATES[j]

            if is_terminal(curr_state):
                curr_state = [curr_state[0], curr_state[1], 0]

            if is_terminal(curr_state):
                print("ERR", file=orig_stdout)

            curr_prob = 1
            agent_pos = curr_state[0]
            
            prob = [(x * curr_prob), ((1-x) * curr_prob)]
            new_states = []
            
            # Stay
            if i == 0:
                prob = [curr_prob]
                curr_state = curr_state
                new_states.append(curr_state)
            # Up
            elif i == 1:

                if isvalid((agent_pos[0], agent_pos[1] + 1)):
                    new_states.append([(agent_pos[0], agent_pos[1] + 1), curr_state[1], curr_state[2]])
                else:
                    new_states.append([(agent_pos[0], agent_pos[1]), curr_state[1], curr_state[2]])
                    
                if isvalid((agent_pos[0], agent_pos[1] - 1)):
                    new_states.append([(agent_pos[0], agent_pos[1] - 1), curr_state[1], curr_state[2]])
                else:
                    new_states.append([(agent_pos[0], agent_pos[1]), curr_state[1], curr_state[2]])

            # Down
            elif i == 2:

                if isvalid((agent_pos[0], agent_pos[1] - 1)):
                    new_states.append([(agent_pos[0], agent_pos[1] - 1), curr_state[1], curr_state[2]])
                else:
                    new_states.append([(agent_pos[0], agent_pos[1]), curr_state[1], curr_state[2]])
                    
                if isvalid((agent_pos[0], agent_pos[1] + 1)):
                    new_states.append([(agent_pos[0], agent_pos[1] + 1), curr_state[1], curr_state[2]])
                else:
                    new_states.append([(agent_pos[0], agent_pos[1]), curr_state[1], curr_state[2]])

            # Left
            elif i == 3:

                if isvalid((agent_pos[0] - 1, agent_pos[1])):
                    new_states.append([(agent_pos[0] - 1 , agent_pos[1]), curr_state[1], curr_state[2]])
                else:
                    new_states.append([(agent_pos[0], agent_pos[1]), curr_state[1], curr_state[2]])
                    
                if isvalid((agent_pos[0] + 1, agent_pos[1])):
                    new_states.append([(agent_pos[0] + 1, agent_pos[1]), curr_state[1], curr_state[2]])
                else:
                    new_states.append([(agent_pos[0], agent_pos[1]), curr_state[1], curr_state[2]])
            # Right
            elif i == 4:
                if isvalid((agent_pos[0] + 1, agent_pos[1])):
                    new_states.append([(agent_pos[0] + 1, agent_pos[1]), curr_state[1], curr_state[2]])
                else:
                    new_states.append([(agent_pos[0], agent_pos[1]), curr_state[1], curr_state[2]])
                    
                if isvalid((agent_pos[0] - 1, agent_pos[1])):
                    new_states.append([(agent_pos[0] - 1, agent_pos[1]), curr_state[1], curr_state[2]])
                else:
                    new_states.append([(agent_pos[0], agent_pos[1]), curr_state[1], curr_state[2]])

            assert(len(new_states)) <= 2
            assert(len(prob)) <= 2

            new_states, prob = emulate_target(new_states, prob)

            sum = 0
            for k in range(len(new_states)):
                probabilities[ret_index(new_states[k])] += prob[k]
                sum += prob[k]

            # print(sum, INITIAL_BELIEF[j], file=orig_stdout)
            assert round(sum, 5) == round(1, 5)

            # print("Action:", ACTIONS[i], "State:", STATES[j], file=orig_stdout)
            T_Action.append(probabilities)
        T.append(T_Action)

    return T

def print_transition(T):

    for i in range(len(T)):
        print("T: ", i)

        matrix = T[i]
        
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                print(matrix[i][j], end=" ")
            print(" ")
        
        print("")

    # print(T[0], file=orig_stdout)

def create_observation_matrix():

    for i in range(len(STATES)):

        curr_state = STATES[i]

        for j in range(6):

            prob = 0

            if j == 0:
                if curr_state[0] == curr_state[1]:
                    prob = 1
            elif j == 1:
                if (curr_state[0][0] + 1, curr_state[0][1]) == curr_state[1]:
                    prob = 1
            elif j == 2:
                if (curr_state[0][0], curr_state[0][1] - 1) == curr_state[1]:
                    prob = 1
            elif j == 3:
                if (curr_state[0][0] - 1, curr_state[0][1]) == curr_state[1]:
                    prob = 1
            elif j == 4:
                if (curr_state[0][0], curr_state[0][1] + 1) == curr_state[1]:
                    prob = 1
            elif j == 5:
                if (abs(curr_state[0][0] - curr_state[1][0]) + abs(curr_state[0][1] - curr_state[1][1])) > 1:
                    prob = 1

            print("O: * :", ret_index(STATES[i]), ":", j, prob)

def create_reward():

    for j in range(len(ACTIONS)):
        for i in range(len(STATES)):
        
            if is_terminal(STATES[i]):
                print("R:", j, " : * :", i, " : * ", rollnumber%100 + 10 - 1)
            else:
                if j == 0:
                    print("R:", j, " : * :", i, " : * ", 0)
                else:
                    print("R:", j, " : * :", i," : * ", -1)
            
def write():

    init_start()
    T = create_transition_matrix()
    print_transition(T)
    create_observation_matrix()
    create_reward()

if __name__ == '__main__':

    output = open(str(rollnumber)+'.pomdp', 'w')

    sys.stdout = output

    print("discount: 0.5")
    print("values: reward")
    print("states:", 162)
    print("actions:", 5)
    print("observations:", 6)

    setup()
    write()

    # for i in range(len(STATES)):
    #     print(STATES[i], file=orig_stdout)

    sys.stdout = orig_stdout
    output.close()