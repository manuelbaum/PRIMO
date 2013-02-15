#!/usr/bin/env python
# -*- coding: utf-8 -*-
from primo.core import BayesNet
from primo.core import DynamicBayesNet
from primo.core import TwoTBN
from primo.reasoning import DiscreteNode
import primo.reasoning.particlebased.ForwardSampling as fs
from primo.reasoning.density import ProbabilityTable
import numpy


#Construct some simple DynmaicBayesianNetwork
B0 = BayesNet()
dbn = DynamicBayesNet()
twoTBN = TwoTBN()

weather0 = DiscreteNode("Weather", ["Rain", "Sun"])
weather = DiscreteNode("Weather", ["Rain", "Sun"])
umbrella0 = DiscreteNode("Umbrella", [True, False])
umbrella = DiscreteNode("Umbrella", [True, False])

B0.add_node(weather0)
B0.add_node(umbrella0)
twoTBN.add_node(weather)
twoTBN.add_node(umbrella)

B0.add_edge(weather0, umbrella0)
twoTBN.add_edge(weather, umbrella)
twoTBN.add_edge(weather, weather, True);

weather0_cpt = numpy.array([.4, .6])
weather0.set_probability_table(weather0_cpt, [weather0])
umbrella0_cpt = numpy.array([[.9, .1], 
                            [.2, .8]])
umbrella0.set_probability_table(umbrella0_cpt, [weather0, umbrella0])

weather_cpt=numpy.array([[.7, .3], 
                         [.5, .5]])
weather.set_probability_table(weather_cpt, [weather, weather])
umbrella_cpt = numpy.array([[.9, .1], 
                            [.2, .8]])
umbrella.set_probability_table(umbrella_cpt, [weather, umbrella])

dbn.set_B0(B0)
dbn.set_TwoTBN(twoTBN)

chain = fs.sample_DBN(dbn, 100000)

pt = ProbabilityTable()
pt.add_variable(weather)
pt.add_variable(umbrella)
pt.to_jpt_by_states(chain)
print "----joint-probability----"
print pt
print "----umbrella----"
print pt.marginalization(umbrella)
#print "----alarm----"
#print pt.division(weather.get_cpd())