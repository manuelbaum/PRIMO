#!/usr/bin/env python
# -*- coding: utf-8 -*-
from primo.core import BayesNet
from primo.core import DynamicBayesNet
from primo.core import TwoTBN
from primo.reasoning import DiscreteNode
import primo.reasoning.particlebased.ParticleFilterDBN as pf
import numpy


#Construct some simple DynmaicBayesianNetwork
B0 = BayesNet()
dbn = DynamicBayesNet()
twoTBN = TwoTBN()

weather0_init = DiscreteNode("Weather0", ["Sun", "Rain"])
weather0 = DiscreteNode("Weather0", ["Sun", "Rain"])
weather = DiscreteNode("Weather", ["Sun", "Rain"])
ice_cream_eaten = DiscreteNode("Ice Cream Eaten", [True, False])

B0.add_node(weather0_init)
twoTBN.add_node(weather0, True)
twoTBN.add_node(weather)
twoTBN.add_node(ice_cream_eaten)

twoTBN.add_edge(weather, ice_cream_eaten)
twoTBN.add_edge(weather0, weather);

cpt_weather0_init = numpy.array([.6, .4])
weather0_init.set_probability_table(cpt_weather0_init, [weather0_init])

cpt_weather0 = numpy.array([.6, .4])
weather0.set_probability_table(cpt_weather0, [weather0])

cpt_weather = numpy.array([[.7, .5],
                           [.3, .5]])
weather.set_probability_table(cpt_weather, [weather0, weather])
ice_cream_eaten.set_probability(.9, [(ice_cream_eaten, True), (weather, "Sun")])
ice_cream_eaten.set_probability(.1, [(ice_cream_eaten, False), (weather, "Sun")])
ice_cream_eaten.set_probability(.2, [(ice_cream_eaten, True), (weather, "Rain")])
ice_cream_eaten.set_probability(.8, [(ice_cream_eaten, False), (weather, "Rain")])

dbn.set_B0(B0)
dbn.set_TwoTBN(twoTBN)

N = 1000
T = 2

time_slice = 0
def get_evidence_function():
    global time_slice
    evidence = {}
    if time_slice == 1:
        time_slice = time_slice + 1
        evidence = {weather:"Rain"}
    else:
        time_slice = time_slice + 1
    print "Time slice " + str(time_slice) + " with evidence " + str(evidence)
    return evidence

samples = pf.particle_filtering_DBN(dbn, N, T, get_evidence_function)
w_hit = 0.0
w_all = 0.0
for i in samples:
    (state, w) = samples[i]
    #print state
    if state[ice_cream_eaten] == True:
        w_hit += w
    w_all += w

print w_all
print w_hit

print("P(..) = " + str(w_hit / w_all))