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
ice_cream_eaten0 = DiscreteNode("Ice Cream eaten", [True, False])
ice_cream_eaten = DiscreteNode("Ice Cream eaten", [True, False])

B0.add_node(weather0)
B0.add_node(ice_cream_eaten0)
twoTBN.add_node(weather)
twoTBN.add_node(ice_cream_eaten)

B0.add_edge(weather0, ice_cream_eaten0)
twoTBN.add_edge(weather, ice_cream_eaten)
twoTBN.add_edge(weather, weather, True);

weather0_cpt = numpy.array([.4, .6])
weather0.set_probability_table(weather0_cpt, [weather0])
ice_cream_eaten0_cpt = numpy.array([[.2, .8],
                                    [.9, .1]])
ice_cream_eaten0.set_probability_table(ice_cream_eaten0_cpt, [weather0, ice_cream_eaten0])

weather_cpt=numpy.array([[.5, .5],
                         [.7, .3]])
weather.set_probability_table(weather_cpt, [weather, weather])
ice_cream_eaten_cpt = numpy.array([[.2, .8],
                                   [.9, .1]])
ice_cream_eaten.set_probability_table(ice_cream_eaten_cpt, [weather, ice_cream_eaten])

dbn.set_B0(B0)
dbn.set_TwoTBN(twoTBN)

#N = 20000
#T = 2
#evidence = [{weather:"Rain"}, {weather:"Sun"}]
#samples = fs.sample_DBN(dbn, N, T, evidence)
#print("P(W_1 = R, W_2 = S) = " + str(len(samples) * 1.0 / N))

N = 1
T = 2
evidence = [{weather: "Rain"}, {ice_cream_eaten: True}]
samples = fs.weighted_sample_DBN(dbn, N, T, evidence)
print("P(W_1 = R, W_2 = S) = " + str(len(samples) * 1.0 / N))

#pt = ProbabilityTable()
#pt.add_variable(weather)
#pt.add_variable(ice_cream_eaten)
#print "---- Joint-Probability ----"
#print pt.to_jpt_by_states(chain)
#print "---- Weather --------------"
#print pt.marginalization(ice_cream_eaten).normalize_as_jpt()
#print "----alarm----"
#print pt.division(weather.get_cpd())