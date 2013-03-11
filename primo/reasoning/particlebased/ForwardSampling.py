# -*- coding: utf-8 -*-
from primo.core import BayesNet
from primo.core import DynamicBayesNet
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

    nodes = network.get_nodes_in_topological_sort()
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
    return state

def weighted_sample(network, events={}, w=1.0, state={}):
    if not isinstance(network, BayesNet):
        raise Exception("The given network is not an instance of BayesNet.")

    nodes = network.get_nodes_in_topological_sort()
    print "---------" + str(w)
    for node in nodes:
        print node
        # reduce this node's cpd
        parents = network.get_parents(node)
        if parents:
            evidence = [(parent, state[parent]) for parent in parents]
            reduced_cpd = node.get_cpd_reduced(evidence)
            print reduced_cpd
        else:
            reduced_cpd = node.get_cpd()

        if node in events:
            print("w before: " + str(w))
            print "foreced state: " + str(events[node])
            w *= reduced_cpd.get_table()[node.get_value_range().index(events[node])]
            state[node] = events[node];
            print("w after: " + str(w))
        else:
            new_state = weighted_random(reduced_cpd.get_table())
            state[node] = node.get_value_range()[new_state]
        print state[node]
    return (state, w)


def sample_DBN(network, N, T, evidence=[]):
    if not isinstance(network, DynamicBayesNet):
        raise Exception("The given network is not an instance of DynamicBayesNet.")

    if len(evidence) != 0 and not len(evidence) == T:
        raise Exception("The list of evidences must have as many entries as " +
        "the number of time slices (T).")

    samples = []
    for n in xrange(N):
        # Sample from initial distribution
        init_state = sample(network.get_B0())

        # Take nodes from 2TBN in state but keep values
        twoTBN = network.get_TwoTBN()
        state = {}
        for node in init_state:
            state[twoTBN.get_node(node.name)] = init_state[node]

        # Sample N Particles
        tmp_sample = []
        tmp_sample.append(copy.copy(state))
        for t in xrange(T - 1):
            state = sample(twoTBN, state)
            tmp_sample.append(copy.copy(state))

        # Reject samples not consistent with evidence
        accept_sample = True
        if len(evidence) != 0:
            for t in xrange(T):
                for node in evidence[t]:
                    if not evidence[t][node] == tmp_sample[t][node]:
                        accept_sample = False

        if accept_sample:
             samples.append(tmp_sample)

    return samples

def weighted_sample_DBN(network, N, T, evidence=[]):
    if not isinstance(network, DynamicBayesNet):
        raise Exception("The given network is not an instance of DynamicBayesNet.")

    if len(evidence) != 0 and not len(evidence) == T:
        raise Exception("The list of evidences must have as many entries as " +
        "the number of time slices (T).")

    samples = []
    w_match = 0.0
    w_all = 0.0
    for n in xrange(N):
        ###
        ### TODO: Solve problem withe evindence for initial and other nodes!
        ###


        # Sample from initial distribution
        (init_state, w) = weighted_sample(network.get_B0(), evidence[0])

        # Take nodes from 2TBN in state but keep values
        twoTBN = network.get_TwoTBN()
        state = {}
        for node in init_state:
            state[twoTBN.get_node(node.name)] = init_state[node]

        # Sample N Particles
        tmp_sample = []
        tmp_sample.append(copy.copy(state))
        for t in xrange(T - 1):
            (state, w) = weighted_sample(twoTBN, evidence[t + 1], w, state)
            tmp_sample.append(copy.copy(state))

        # Reject samples not consistent with evidence
        accept_sample = True
        if len(evidence) != 0:
            for t in xrange(T):
                for node in evidence[t]:
                    if not evidence[t][node] == tmp_sample[t][node]:
                        accept_sample = False

        if accept_sample:
             samples.append(tmp_sample)
             w_match += w
        w_all += w

    print(str(w_match/w_all))
    return samples
