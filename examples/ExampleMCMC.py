#!/usr/bin/env python
# -*- coding: utf-8 -*-
from  primo.core import BayesNet
from  primo.reasoning import DiscreteNode
from  primo.reasoning import MarkovChainSampler
from primo.reasoning import GibbsTransitionModel
from primo.reasoning.density import ProbabilityTable
import numpy
import pdb

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
#print pt.division(burglary.get_cpd())

print "----ProbabilityOfEvidence----"
evidence={burglary:"Intruder"}
chain = mcs.generateMarkovChain(bn, 5000, transition_model, initial_state)
compatible_count=0
number_of_samples=0
for state in chain:
    compatible = True
    for node,value in evidence.items():
        
        if state[node] != value:
            compatible = False
            break
    print compatible
    if compatible:
        compatible_count = compatible_count + 1
    
    number_of_samples = number_of_samples + 1

print compatible_count
print number_of_samples
probability_of_evidence = float(compatible_count)/float(number_of_samples)
print probability_of_evidence


print "----EVIDENCE: burglary=Intruder----"
evidence={burglary:"Intruder"}
initial_state={burglary:"Intruder",alarm:"Silent"}
chain = mcs.generateMarkovChain(bn, 5000, transition_model, initial_state, evidence)
pt.to_jpt_by_states(chain)
print pt


