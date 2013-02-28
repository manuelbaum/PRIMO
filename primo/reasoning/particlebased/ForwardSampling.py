# -*- coding: utf-8 -*-
from primo.core import BayesNet
from primo.core import DynamicBayesNet
from primo.core import TwoTBN
import random
import copy

def weighted_random(weights):
    counter = random.random() * sum(weights)
    for i, w in enumerate(weights):
        counter -= w
        if counter <= 0:
            return i

def sample(network, state={}):
    if not isinstance(network, BayesNet):
        raise Exception("The given network is not an instance of BayesNet.")

    if not isinstance(network, TwoTBN):
        nodes = network.get_nodes_in_topological_sort()
    else:
        nodes = network.get_nodes()
    #print("#### Sampling ####")
    for node in nodes:
        # reduce this node's cpd
        parents = network.get_parents(node)
        if parents:
            evidence = [(parent, state[parent]) for parent in parents]
            reduced_cpd = node.get_cpd_reduced(evidence)
        else:
            reduced_cpd = node.get_cpd()

        new_state = weighted_random(reduced_cpd.get_table())
        state[node] = node.get_value_range()[new_state]
        #print("Node: " + node.name + " (" + str(state[node]) + ")")
    #print("#### Sampling done ####")
    return state

def sample_DBN(network, N, T, evidence=[]):
    if not isinstance(network, DynamicBayesNet):
        raise Exception("The given network is not an instance of DynamicBayesNet.")

    if len(evidence) != 0 and not len(evidence) == T:
        raise Exception("The list of evidences must have as many entries as " +
        "the number of time slices (T).")

    samples = {}
    for n in xrange(N):
        #print("###### Sample " + str(n) + " ######")
        # Sample from initial distribution
        init_state = sample(network.get_B0())

        # Copy nodes from 2TBN in state but keep values
        twoTBN = network.get_TwoTBN()
        state = {}
        #print("### Initial state ###")
        for node in init_state:
            #print(str(node.name) + ": " + str(init_state[node]))
            state[twoTBN.get_node(node.name)] = init_state[node]

        # Sample N Particles
        tmp_sample = []
        tmp_sample.append(copy.copy(state))
        for t in xrange(T - 1):
            #yield state
            state = sample(twoTBN, state)
            tmp_sample.append(copy.copy(state))

        #for i in xrange(len(tmp_sample)):
        #    state = tmp_sample[i]
        #    for node in state:
        #        print("Node: " + node.name + " (" + str(state[node]) + ")")

        accept_sample = True
        for t in xrange(T):
            for node in evidence[t]:
                if not evidence[t][node] == tmp_sample[t][node]:
                    accept_sample = False

        if accept_sample:
             samples[n] = tmp_sample

    return samples