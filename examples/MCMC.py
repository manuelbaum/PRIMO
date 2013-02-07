#!/usr/bin/env python
# -*- coding: utf-8 -*-
from  primo.core import BayesNet
from  primo.reasoning import DiscreteNode
from  primo.reasoning import MarkovChainSampler
from primo.reasoning import GibbsTransitionModel
from primo.reasoning.density import ProbabilityTable
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
chain = mcs.generateMarkovChain(bn, 5000, transition_model, initial_state)

#for c in chain:
#    print c


pt = ProbabilityTable()
pt.add_variable(burglary)
pt.add_variable(alarm)
pt.to_jpt_by_states(chain)
print "----joint-probability----"
print pt
print "----burglary----"
print pt.marginalization(alarm)
print "----alarm----"
print pt.division(burglary.get_cpd())

bn.draw()

