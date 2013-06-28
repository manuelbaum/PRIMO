#!/usr/bin/env python
# -*- coding: utf-8 -*-
from  primo.core import BayesNet
from  primo.reasoning import DiscreteNode
from primo.reasoning.density import ProbabilityTable
from primo.reasoning import MCMC
from primo.reasoning import EvidenceEqual as EvEq
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




mcmc_ask=MCMC(bn)

evidence={burglary:EvEq("Intruder")}


print "---ProbabilityOfEvidence:---" 
poe=mcmc_ask.calculate_PoE(evidence)
print poe

print "---PosteriorMarginal:---"
pm=mcmc_ask.calculate_PosteriorMarginal([alarm],evidence,ProbabilityTable)
print pm

print "---PriorMarginal:---"
pm=mcmc_ask.calculate_PriorMarginal([alarm],ProbabilityTable)
print "Alarm: " + str(pm)
pm=mcmc_ask.calculate_PriorMarginal([burglary],ProbabilityTable)
print "Burglary: " + str(pm)

print "---MAP:---"
hyp=mcmc_ask.calculate_MAP([alarm],evidence,ProbabilityTable)
print str(evidence) + ": " + str(hyp)
hyp=mcmc_ask.calculate_MAP([alarm],{},ProbabilityTable)
print str({}) + ": "+str(hyp)
