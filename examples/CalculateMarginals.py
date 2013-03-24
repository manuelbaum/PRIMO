# -*- coding: utf-8 -*-
"""
This example show how to calculate Marginals and 
the probility of evidence.

@author: djohn
"""

from  primo.core import BayesNet
from  primo.reasoning import DiscreteNode
from primo.reasoning.factorelemination import EasiestFactorElimination
from primo.reasoning.factorelemination import FactorTreeFactory
import numpy

#==============================================================================
#Builds the example BayesNet
bn = BayesNet()
burglary = DiscreteNode("Burglary", ["Intruder","Safe"])
alarm = DiscreteNode("Alarm", ["Ringing", "Silent"])
earthquake = DiscreteNode("Earthquake", ["Shaking", "Calm"])
john_calls = DiscreteNode("John calls", ["Calling", "Not Calling"])
baum_calls = DiscreteNode("Baum calls", ["Calling", "Not Calling"])

bn.add_node(burglary)
bn.add_node(alarm)
bn.add_node(earthquake)
bn.add_node(john_calls)
bn.add_node(baum_calls)

bn.add_edge(burglary,alarm)
bn.add_edge(earthquake, alarm)
bn.add_edge(alarm, john_calls)
bn.add_edge(alarm, baum_calls)

cpt_burglary = numpy.array([0.001,0.999])
burglary.set_probability_table(cpt_burglary,[burglary])

cpt_earthquake = numpy.array([0.002,0.998])
earthquake.set_probability_table(cpt_earthquake,[earthquake])

alarm.set_probability(0.95,[(alarm,"Ringing"),(burglary,"Intruder"),(earthquake,"Shaking")])
alarm.set_probability(0.05,[(alarm,"Silent"),(burglary,"Intruder"),(earthquake,"Shaking")])
alarm.set_probability(0.29,[(alarm,"Ringing"),(burglary,"Safe"),(earthquake,"Shaking")])
alarm.set_probability(0.71,[(alarm,"Silent"),(burglary,"Safe"),(earthquake,"Shaking")])
alarm.set_probability(0.94,[(alarm,"Ringing"),(burglary,"Intruder"),(earthquake,"Calm")])
alarm.set_probability(0.06,[(alarm,"Silent"),(burglary,"Intruder"),(earthquake,"Calm")])
alarm.set_probability(0.001,[(alarm,"Ringing"),(burglary,"Safe"),(earthquake,"Calm")])
alarm.set_probability(0.999,[(alarm,"Silent"),(burglary,"Safe"),(earthquake,"Calm")])

baum_calls.set_probability(0.9,[(alarm,"Ringing"),(baum_calls,"Calling")])
baum_calls.set_probability(0.1,[(alarm,"Ringing"),(baum_calls,"Not Calling")])
baum_calls.set_probability(0.05,[(alarm,"Silent"),(baum_calls,"Calling")])
baum_calls.set_probability(0.95,[(alarm,"Silent"),(baum_calls,"Not Calling")])

john_calls.set_probability(0.7,[(alarm,"Ringing"),(john_calls,"Calling")])
john_calls.set_probability(0.3,[(alarm,"Ringing"),(john_calls,"Not Calling")])
john_calls.set_probability(0.01,[(alarm,"Silent"),(john_calls,"Calling")])
john_calls.set_probability(0.99,[(alarm,"Silent"),(john_calls,"Not Calling")])

#==============================================================================
# This Factor Elimination at first builds the joint probability table (jpt) and
# then projects on the queried variables

fe = EasiestFactorElimination()
fe.set_BayesNet(bn)
print "===== Easiest Factor Elimination ======"
print "Prior Alarm:   " + str(fe.calculate_PriorMarginal([alarm]))
print "Prior John_Calls: " + str(fe.calculate_PriorMarginal([john_calls]))
print "Prior Baum_Calls: " + str(fe.calculate_PriorMarginal([baum_calls]))
print "Prior Burglary: " + str(fe.calculate_PriorMarginal([burglary]))
print "Prior Earthquake: " + str(fe.calculate_PriorMarginal([earthquake]))

print "PoE Earthquake: " + str(fe.calculate_PoE([(earthquake, "Calm")]))
print "PoE BaumCalls is Calling: " + str(fe.calculate_PoE([(baum_calls, "Calling")]))

print "Posterior of burglary : " + str(fe.calculate_PosteriorMarginal([burglary],[(alarm, "Ringing"),(earthquake, "Calm")]))

factorTreeFactory = FactorTreeFactory()
factorTree = factorTreeFactory.create_greedy_factortree(bn)

print "====Factor Tree===="

print "Prior Marginal:"

print "AlarmFT: " + str(factorTree.calculate_marginal([alarm]))
print "John_CallsFT: " + str(factorTree.calculate_marginal([john_calls]))
print "Baum_CallsFT: " + str(factorTree.calculate_marginal([baum_calls]))
print "BurglaryFT: " + str(factorTree.calculate_marginal([burglary]))
print "EarthquakeFT: " + str(factorTree.calculate_marginal([earthquake]))

factorTree.set_evidences([(alarm, "Ringing"),(earthquake, "Calm")])

print "PoE: " + str(factorTree.calculate_PoE())

print "Posterior Marginal (alarm->ringing , earthquake->calm):"

print "AlarmFT: " + str(factorTree.calculate_marginal([alarm]))
print "John_CallsFT: " + str(factorTree.calculate_marginal([john_calls]))
print "Baum_CallsFT: " + str(factorTree.calculate_marginal([baum_calls]))
print "BurglaryFT: " + str(factorTree.calculate_marginal([burglary]))
print "EarthquakeFT: " + str(factorTree.calculate_marginal([earthquake]))

#factorTree.draw()


            
#factorTree.draw()