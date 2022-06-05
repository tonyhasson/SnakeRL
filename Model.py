import random

def build_action_vector(state):  ##for now until real model is built
    ##create random list of action(later will be a ML model)
    print(state)
    num = random.randint(1, 3)
    if num == 1:
        return [1, 0, 0]
    elif num == 2:
        return [0, 1, 0]
    elif num == 3:
        return [0, 0, 1]

