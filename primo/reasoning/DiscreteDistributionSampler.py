# -*- coding: utf-8 -*-

def weighted_random(self, weights):
    import random
    counter = random.random() * sum(weights)
    for i, w in enumerate(weights):
        counter -= w
        if counter <= 0:
            return i