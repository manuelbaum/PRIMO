#!/usr/bin/env python
# -*- coding: utf-8 -*-
from  primo.core import BayesNet
from  primo.reasoning import DiscreteNode
from  primo.reasoning import MarkovChainSampler
from primo.reasoning import GibbsTransitionModel
import numpy

#Construct some simple BayesianNetwork
bn = BayesNet()
burglary = DiscreteNode("Burglary", ["Intruder","Safe"])
alarm = DiscreteNode("Alarm", ["Ringing", "Silent","Kaputt"])

bn.add_node(burglary)
bn.add_node(alarm)

bn.add_edge(burglary,alarm)

burglary_cpt=numpy.array([0.2,0.8])
burglary.set_probability_table(burglary_cpt, [burglary])

alarm_cpt=numpy.array([[0.8,0.15,0.05],[0.05,0.9,0.05]])
alarm.set_probability_table(alarm_cpt, [burglary,alarm])

#Construct a Markov Chain by sampling states from this Network

transition_model = GibbsTransitionModel()

mcs = MarkovChainSampler()
initial_state={burglary:"Safe",alarm:"Silent"}
chain = mcs.generateMarkovChain(bn, 20, transition_model, initial_state)

for c in chain:
    print c
