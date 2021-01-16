import pickle
from local_settings import *
from colorama import Fore
import math

def pluraity_value(examples):

    positive = 0
    negative = 0

    for i in range(len(examples)):
        if examples[i]["kill"]:
            positive += 1
        else:
            negative += 1

    if positive > negative:
        return True
    else:
        return False

def sort(attribute, examples):
    for i in range(len(examples)):
        for j in range(0, len(examples) - i - 1):
            if float(examples[j][attribute]) > float(examples[j+1][attribute]):
                examples[j], examples[j+1] = examples[j+1], examples[j]

    return examples

def calc_entropy(q):
    if q == 0 or q == 1:
        return 0
    val = -(q*math.log2(q) + (1-q)*math.log(1-q))
    return val

def calc_parent_entropy(examples):
    positive = 0
    negative = 0

    for i in range(len(examples)):
        if examples[i]["kill"]:
            positive += 1
        else:
            negative += 1


    return calc_entropy(positive/(positive + negative))

def calc_remainder(positive, negative, parent_examples):

    positive_p = 0
    negative_p = 0

    for i in range(len(parent_examples)):
        if parent_examples[i]["kill"]:
            positive_p += 1
        else:
            negative_p += 1

    assert (positive_p + negative_p) > 0

    tot = 0
    for i in range(len(positive)):
        tot += (((positive[i] + negative[i]) / (positive_p + negative_p)) * calc_entropy(positive[i]/(positive[i] + negative[i])))

    return tot

def importance(attribute, examples, parent_examples):

    examples = sort(attribute, examples)
    max_i = -100
    max_gain = -100

    for i in range(1, len(examples)):

        positive = [0, 0]
        negative = [0, 0]

        for j in range(len(examples)):
            if float(examples[j][attribute]) < float(examples[i][attribute]):
                if examples[j]["kill"]:
                    positive[0] += 1
                else:
                    negative[0] += 1
            else:
                if examples[j]["kill"]:
                    positive[1] += 1
                else:
                    negative[1] += 1

        remainder = calc_remainder(positive, negative, examples)
        gain = calc_parent_entropy(examples) - remainder
        
        assert gain >= 0

        if gain > max_gain:
            max_gain = gain
            max_i = i

    return max_gain, max_i

def max_importance(attributes, examples, parent_examples):

    max_gain = -100
    split_point = -100
    attribute = attributes[0]

    for i in range(len(attributes) - 1):
        examples = sort(attributes[i], examples)
        if importance(attributes[i], examples, parent_examples)[0] > max_gain:
            attribute = attributes[i]
            max_gain, split_point = importance(attributes[i], examples, parent_examples)

    examples = sort(attribute, examples)

    print("-----------------")

    return attribute, split_point

def all_same(examples):
    val = examples[0]["kill"]
    for i in range(len(examples)):
        if examples[i]["kill"] != val:
            return False
    print(">-------------")
    print(examples)
    print("All Same\n")
    print("<------------")
    return True

def decision_tree_learning(depth, examples, attributes, parent_examples):

    # print(examples)

    if len(examples) == 0:
        print("No examples left.")
        return pluraity_value(parent_examples)
    elif all_same(examples):
        return True
    elif len(attributes) == 1:
        print("No attributes left.")
        print(examples)
        return pluraity_value(examples)
    else:
        A, split_value = max_importance(attributes, examples, parent_examples)
        print(">-----------")
        print("Attribute is " + A)
        print("Split Value is " + str(split_value))
        examples = sort(A, examples)
        sets = [examples[:split_value], examples[split_value:]]

        new_attributes = []
        for i in range(len(attributes)):
            # if attributes[i] != A:
            if attributes[i]=="angle" and depth==2:
                continue
            new_attributes.append(attributes[i])

        for i in range(len(sets)):
            subtree = decision_tree_learning(depth+1, sets[i], new_attributes, sets[i])
        print("<-----------")
 
if __name__ == "__main__":
    decision_tree_learning(1, EXAMPLES, ATTRIBUTES, EXAMPLES)