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
alarm = DiscreteNode("Alarm", ["Ringing", "Silent","Destroyed"])

bn.add_node(burglary)
bn.add_node(alarm)

bn.add_edge(burglary,alarm)


#Parametrize the network
burglary_cpt=numpy.array([0.2,0.8])
burglary.set_probability_table(burglary_cpt, [burglary])

alarm_cpt=numpy.array([[0.8,0.15,0.05],[0.05,0.9,0.05]])
alarm.set_probability_table(alarm_cpt, [burglary,alarm])


#Get some inference object
mcmc_ask=MCMC(bn,5000)

#Do some Inferences
evidence={burglary:EvEq("Intruder")}

print "-------ProbabilityOfEvidence:-------" 
poe=mcmc_ask.calculate_PoE(evidence)
print "p(evidence=Intruder)="+str(poe)
print "Ground truth=0.2\n"

print "-------PosteriorMarginal:-------"
pm=mcmc_ask.calculate_PosteriorMarginal([alarm],evidence,ProbabilityTable)
print "P(alarm|burglary=Intruder)="+str(pm)
print "Ground truth=[0.8, 0.15, 0.05]\n"

print "-------PriorMarginal:-------"
pm=mcmc_ask.calculate_PriorMarginal([alarm],ProbabilityTable)
print "P(Alarm)= " + str(pm)
print "Ground truth=[0.2, 0.75, 0.05]\n"

pm=mcmc_ask.calculate_PriorMarginal([burglary],ProbabilityTable)
print "P(Burglary)= " + str(pm)
print "Ground truth=[0.2, 0.8]\n"

print "-------MAP:-------"
hyp=mcmc_ask.calculate_MAP([alarm],evidence,ProbabilityTable)
print "MAP(alarm|burglary=intruder)=" + str(hyp)
print "Ground truth=\"Ringing\"\n"

hyp=mcmc_ask.calculate_MAP([burglary,alarm],{},ProbabilityTable)
print "MAP(burglary,alarm)="+str(hyp)
print "Ground truth=\"Safe\",\"Silent\"\n"
