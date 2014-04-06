#!/usr/bin/env python
# -*- coding: utf-8 -*-
from primo.networks import BayesianNetwork
from primo.nodes import DiscreteNode
from primo.densities import ProbabilityTable
from primo.inference.mcmc import MCMC
from primo.evidence import EvidenceEqual as EvEq
from primo.inference.mcmc import GibbsTransitionModel
import numpy
import pdb

#About this example:
#This example shows how approximate inference can be used query a purely discrete
#bayesian network. At first that network is being constructed and afterwards it
#is passed to an MCMC object that is used to answer several kinds of questions:
#-Prior marginal
#-Posterior marginal
#-Probability of evidence
#-Maximum a-posteriori hypothesis

#Construct some simple BayesianNetwork
bn = BayesianNetwork()
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
mcmc_ask=MCMC(bn,5000,transition_model=GibbsTransitionModel())

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
