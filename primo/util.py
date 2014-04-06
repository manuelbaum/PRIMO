import random

def weighted_random(weights):
    '''
    Implements roulette-wheel-sampling.
    @param weights: A List of float-values.
    @returns: Index of the selected entity
    '''
    counter = random.random() * sum(weights)
    for i, w in enumerate(weights):
        counter -= w
        if counter <= 0:
            return i