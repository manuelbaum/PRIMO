# -*- coding: utf-8 -*-
from primo.core import BayesNet
from primo.core import DynamicBayesNet
import random
import copy
import time

def weighted_random(weights):
    counter = random.random() * sum(weights)
    for i, w in enumerate(weights):
        counter -= w
        if counter <= 0:
            return i

def wighted_sample_with_replacement(samples = {}, weights = [], N = 0):
    ws_sum = sum(weights)
    new_samples = {}
    for n in xrange(N):
        r = random.random() * ws_sum
        for i, w in enumerate(weights):
            r -= w
            if r <= 0:
                new_samples[n] = (samples[i], w);
                break
    return new_samples

def weighted_sample(network, evidence = {}):
    w = 1.0
    state = {}
    if not isinstance(network, BayesNet):
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
        # sample state
        new_state = weighted_random(reduced_cpd.get_table())
        state[node] = node.get_value_range()[new_state]
        
        # (re-)calulate weight
        if node in evidence:
            w *= reduced_cpd.get_table()[node.get_value_range().index(evidence[node])]
    return (state, w)

def gibs_sample(network, state, events = {}):
    w = 1.0
    if not isinstance(network, BayesNet):
        raise Exception("The given network is not an instance of BayesNet.")
    nodes = network.get_nodes_in_topological_sort()
    for node in nodes:
        # reduce this node's cpd
        parents = network.get_parents(node)
        if parents:
            evidence = [(parent, state[parent]) for parent in parents]
            reduced_cpd = node.get_cpd_reduced(evidence)
        else:
            reduced_cpd = node.get_cpd()
        
        #reduce the children's cpds
        children = network.get_children(node)
        for child in children:
            parents = network.get_parents(child)
            evidence = [(parent, state[parent]) for parent in parents if parent != node]
            evidence.append((child, state[child]))
            reduced_child_cpd = child.get_cpd_reduced(evidence)
            reduced_cpd = reduced_cpd.multiplication(reduced_child_cpd)
        # sample state
        new_state = weighted_random(reduced_cpd.get_table())
        state[node] = node.get_value_range()[new_state]       
        
        # (re-)calulate weight
        if node in events:
            w *= reduced_cpd.get_table()[node.get_value_range().index(evidence[node])]
    return (state, w)

def particle_filtering_DBN(network, N, T, get_evidence_function, interval = 0):
    '''
    Create N samples for the given network with T time slices.

    Keyword arguments:
    network -- a DynamicBayesNet
    N -- number of samples
    T -- number of time slices (set -1 for infinite loop)
    get_evidence_function -- a function that returns a dict with the following
    structure: {node1:evidence1, node2:evidence2, ...}
    interval -- time to sleep between two sample loops (only if T = -1)

    Returns a dict of N samples
    '''
    if not isinstance(network, DynamicBayesNet):
        raise Exception("The given network is not an instance of DynamicBayesNet.")

    if not network.is_valid():
        raise Exception("The given network is not valid.")

    # Sample from inital distribution
    samples = sample_from_inital_distribution(network, get_evidence_function(), N)

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

#    return samples

def sample_from_inital_distribution(network, evidence, N):
    '''
    Create samples from initial distribution.

    Keyword arguments:
    network -- a DynamicBayesNet
    evidence -- dict with the following structure: {node1:evidence1, node2:evidence2, ...}
    N -- number of samples

    Returns a dict of N samples
    '''
    samples = {}
    weights = []
    for n in xrange(N):
        # Sample from inital distribution
        (state, w) = weighted_sample(network.B0, evidence)
        samples[n] = copy.copy(state)
        weights.append(w)
    
    weights = normalize_weights(weights)    
    
    # wighted sample with replacement
    return wighted_sample_with_replacement(samples, weights, N)


def sample_one_time_slice(network, samples, evidence, initial_samples = False, gibbs = False, gibbs_iterations = 5):
    '''
    Create samples for next time slice

    Keyword arguments:
    network -- a DynamicBayesNet
    samples -- a dict of samples (sampled from initial distribution at the beginning or a previous time slice)
    evidence -- dict with the following structure: {node1:evidence1, node2:evidence2, ...}
    initial_samples -- is true if the given samples where sampled from the initial distribution
    Returns a dict of N new samples
    '''
    weights = []
    twoTBN = network.twoTBN
    N = len(samples)
    for i in xrange(N):
        (state, w) = samples[i]
        ts = twoTBN.create_timeslice(state, initial_samples)
        (state, w) = weighted_sample(ts, evidence)
        if gibbs:
            for g in xrange(gibbs_iterations):
                (state, w) = gibs_sample(ts, state, evidence)

        samples[i] = copy.copy(state)
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
