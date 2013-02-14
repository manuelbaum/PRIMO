#!/usr/bin/env python
# -*- coding: utf-8 -*-
from  primo.core import BayesNet
from  primo.reasoning import DiscreteNode
from primo.reasoning.factorelemination import EasiestFactorElimination
import numpy

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


cpt_burglary = numpy.array([0.002,0.998])
burglary.set_probability_table(cpt_burglary,[burglary])

cpt_earthquake = numpy.array([0.001,0.999])
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



#first Elimination:
fe = EasiestFactorElimination()
fe.set_BayesNet(bn)
#print "Alarm: " + str(fe.calculate_PriorMarginal([alarm]))
#print "John_Calls: " + str(fe.calculate_PriorMarginal([john_calls]))
#print "Baum_Calls: " + str(fe.calculate_PriorMarginal([baum_calls]))
#print "Burglary: " + str(fe.calculate_PriorMarginal([burglary]))
#print "Earthquake: " + str(fe.calculate_PriorMarginal([earthquake]))

#print "PoE Earthquake: " + str(fe.calculate_PoE([(earthquake, "Calm")]))
#print "PoE BaumCalls is Calling: " + str(fe.calculate_PoE([(baum_calls, "Calling")]))

