# -*- coding: utf-8 -*-

import copy
import random
import time

import primo.networks
from primo.util import weighted_random

class Particle(object):
    '''
    This is the basic particle class used by the DBN particle filter.
    Inherit this class for more functionality.
    '''
    def __init__(self):
        self.state = None

    def set_state(self, state):
        '''
        Set the state of this particle and call the update() function.

        Keyword arguments:
        state -- new state of this particle
        '''
        self.state = state
        self.update()

    def get_state(self):
        '''
        Get the state of this particle.

        Returns the state of this particle.
        '''
        return self.state

    def update(self):
        '''
        Implement this method to update the particle as required.
        '''
        pass

def wighted_sample_with_replacement(samples = [], weights = [], N = 0):
    '''
    The population is resampled to generate a new population of N samples.
    Each new sample is selected from the current population; the probability
    that a particular sample is selected is proportional to its weight.

    See "Artificial Intelligence: A Modern Approach (Third edition)" by
    Stuart Russell and Peter Norvig (p. 596 ff.)

    Keyword arguments:
    samples -- a vector/list of samples of size N
    weights -- a vector/list of weights of size N
    N -- number of samples to be maintained

    Returns a vector/list with new samples.
    '''
    ws_sum = sum(weights)
    new_samples = []
    for n in xrange(N):
        r = random.random() * ws_sum
        for i, w in enumerate(weights):
            r -= w
            if r <= 0:
                new_samples.append(copy.copy(samples[i]));
                break
    return new_samples

def weighted_sample(network, evidence = {}):
    '''
    Each nonevidence variable is sampled according to the conditional
    distribution given the values already sampled for the variable's parents,
    while a weight isaccumulated based on the likelihood for each evidence
    variable.

    See "Artificial Intelligence: A Modern Approach (Third edition)" by
    Stuart Russell and Peter Norvig (p. 534)

    Keyword arguments:
    network -- a Bayesian network
    evidence -- a dict of observed values

    Returns a new sample as tuple of state and weight (state, w).
    '''
    w = 1.0
    state = {}
    if not isinstance(network, primo.networks.BayesianNetwork):
        raise Exception("The given network is not an instance of BayesNet.")

    nodes = network.get_nodes_in_topological_sort()
    for node in nodes:
        #reduce this node's cpd
        parents = network.get_parents(node)
        if parents:
            evidence_tmp = [(parent, state[parent]) for parent in parents]
            reduced_cpd = node.get_cpd_reduced(evidence_tmp)
        else:
            reduced_cpd = node.get_cpd()

        # (re-)calulate weight
        if node in evidence:
            w *= reduced_cpd.get_table()[node.get_value_range().index(evidence[node])]
            state[node] = node.get_value_range().index(evidence[node])
        else:
            # sample state
            new_state = weighted_random(reduced_cpd.get_table())
            state[node] = node.get_value_range()[new_state]

    return (state, w)

def particle_filtering_DBN(network, N, T, get_evidence_function, particle_class = Particle, interval = 0):
    '''
    Create N samples for the given network with T time slices.

    See "Artificial Intelligence: A Modern Approach (Third edition)" by
    Stuart Russell and Peter Norvig (p. 596 ff.)

    Keyword arguments:
    network -- a DynamicBayesNet
    N -- number of samples
    T -- number of time slices (set -1 for infinite loop)
    get_evidence_function -- a function that returns a dict with the following
    structure: {node1:evidence1, node2:evidence2, ...}
    interval -- time to sleep between two sample loops (only if T = -1)

    Returns a list of N samples
    '''
    if not isinstance(network, primo.networks.DynamicBayesianNetwork):
        raise Exception("The given network is not an instance of DynamicBayesNet.")

    if not network.is_valid():
        raise Exception("The given network is not valid.")

    # Sample from inital distribution
    samples = sample_from_inital_distribution(network, get_evidence_function(), N, particle_class)

    # Sample time slices
    initial_samples = True
    if T == -1:
        while True:
            yield samples
            if initial_samples:
                samples = sample_one_time_slice(network, samples, get_evidence_function(), True)
                initial_samples = False
            else:
                samples = sample_one_time_slice(network, samples, get_evidence_function())
            time.sleep(interval)
    else:
        for t in xrange(0, T):
            yield samples
            if initial_samples:
                samples = sample_one_time_slice(network, samples, get_evidence_function(), True)
                initial_samples = False
            else:
                samples = sample_one_time_slice(network, samples, get_evidence_function())


def sample_from_inital_distribution(network, evidence, N, particle_class = Particle):
    '''
    Create samples from initial distribution.

    Keyword arguments:
    network -- a DynamicBayesNet
    evidence -- dict with the following structure: {node1:evidence1, node2:evidence2, ...}
    N -- number of samples

    Returns a list of N samples
    '''
    samples = []
    weights = []
    for n in xrange(N):
        # Sample from inital distribution
        (state, w) = weighted_sample(network.B0, evidence)
        samples.append(particle_class())
        samples[n].set_state(copy.copy(state))
        weights.append(w)

    weights = normalize_weights(weights)

    # wighted sample with replacement
    return wighted_sample_with_replacement(samples, weights, N)


def sample_one_time_slice(network, samples, evidence, initial_samples = False):
    '''
    Create samples for next time slice

    Keyword arguments:
    network -- a DynamicBayesNet
    samples -- a dict of samples (sampled from initial distribution at the beginning or a previous time slice)
    evidence -- dict with the following structure: {node1:evidence1, node2:evidence2, ...}
    initial_samples -- is true if the given samples where sampled from the initial distribution

    Returns a list of N new samples
    '''
    weights = []
    twoTBN = network.twoTBN
    N = len(samples)
    for n in xrange(N):
        state = samples[n].get_state()
        ts = twoTBN.create_timeslice(state, initial_samples)
        (state, w) = weighted_sample(ts, evidence)

        samples[n].set_state(copy.copy(state))
        weights.append(w)

    weights = normalize_weights(weights)

    # wighted sample with replacement
    return wighted_sample_with_replacement(samples, weights, N)

def normalize_weights(weights=[]):
    '''
    Normalize the given weights.

    Keyword arguments:
    weights -- a list of weights

    Returns a list of normalized weights
    '''
    n = sum(weights)
    for (i, w) in enumerate(weights):
        weights[i] = w * 1.0 / n
    return weights
