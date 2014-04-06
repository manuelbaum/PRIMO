# -*- coding: utf-8 -*-
"""
This example show how to calculate Marginals and 
the probability of evidence.

@author: djohn
"""

from primo.networks import BayesianNetwork
from primo.nodes import DiscreteNode
from primo.inference.factor import EasiestFactorElimination
from primo.inference.factor import FactorTreeFactory
import numpy

#==============================================================================
#Builds the example BayesNet
bn = BayesianNetwork()
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
# The EasiestFactorElimination first builds the joint probability table (jpt) and
# then projects on the queried variables

fe = EasiestFactorElimination(bn)
#For very small BayesNets this is the fastest calculation

print "===== Easiest Factor Elimination ======"
print "Prior Alarm:   " + str(fe.calculate_PriorMarginal([alarm]))
print "Prior John_Calls: " + str(fe.calculate_PriorMarginal([john_calls]))
print "Prior Baum_Calls: " + str(fe.calculate_PriorMarginal([baum_calls]))
print "Prior Burglary: " + str(fe.calculate_PriorMarginal([burglary]))
print "Prior Earthquake: " + str(fe.calculate_PriorMarginal([earthquake]))

print "PoE Earthquake: " + str(fe.calculate_PoE([(earthquake, "Calm")]))
print "PoE BaumCalls is Calling: " + str(fe.calculate_PoE([(baum_calls, "Calling")]))

print "Posterior of burglary : " + str(fe.calculate_PosteriorMarginal([burglary],[(alarm, "Ringing"),(earthquake, "Calm")]))

#==============================================================================

factorTreeFactory = FactorTreeFactory()
factorTree = factorTreeFactory.create_greedy_factortree(bn)
factorTree.draw()

#For large nets or much queries the factorTree is the most efficient way.
#The first query is expensive in calculation but all following queries are very 
#fast calculated.
#When you set or clear evidence all stored values need to be recalculated. Thus,
# after changing evidence the first query is again expensive in calculation.

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

#Ausgabe:
#===== Easiest Factor Elimination ======
#Prior Alarm:   [ 0.00251644  0.99748356]
#Prior John_Calls: [ 0.01173634  0.98826366]
#Prior Baum_Calls: [ 0.05213898  0.94786102]
#Prior Burglary: [ 0.001  0.999]
#Prior Earthquake: [ 0.002  0.998]
#PoE Earthquake: 0.998
#PoE BaumCalls is Calling: 0.0521389757
#Posterior of burglary : [ 0.48478597  0.51521403]
#====Factor Tree====
#Prior Marginal:
#AlarmFT: [ 0.00251644  0.99748356]
#John_CallsFT: [ 0.01173634  0.98826366]
#Baum_CallsFT: [ 0.05213898  0.94786102]
#BurglaryFT: [ 0.001  0.999]
#EarthquakeFT: [ 0.002  0.998]
#PoE: 0.001935122
#Posterior Marginal (alarm->ringing , earthquake->calm):
#AlarmFT: [ 1.  0.]
#John_CallsFT: [ 0.7  0.3]
#Baum_CallsFT: [ 0.9  0.1]
#BurglaryFT: [ 0.48478597  0.51521403]
#EarthquakeFT: [ 0.  1.]

