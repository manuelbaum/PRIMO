#!/usr/bin/env python
# -*- coding: utf-8 -*-
from  primo.networks import BayesianNetwork
from  primo.nodes import DiscreteNode
import numpy

bn = BayesianNetwork()
burglary = DiscreteNode("Burglary", ["Intruder","Safe"])
alarm = DiscreteNode("Alarm", ["Ringing", "Silent","Kaputt"])
earthquake = DiscreteNode("Earthquake", ["Shaking", "Calm"])
john_calls = DiscreteNode("John calls", ["Calling", "Not Calling"])
mary_calls = DiscreteNode("Mary calls", ["Calling", "Not Calling"])


bn.add_node(burglary)
bn.add_node(alarm)
bn.add_node(earthquake)
bn.add_node(john_calls)
bn.add_node(mary_calls)


bn.add_edge(burglary,alarm)
bn.add_edge(earthquake, alarm)
bn.add_edge(alarm, john_calls)
bn.add_edge(alarm, mary_calls)


burglary.set_probability(0.2,[(burglary,"Intruder")])

alarm.set_probability(0.1,[(alarm,"Ringing"),(burglary,"Safe"),(earthquake,"Calm")])

cpt = numpy.array([[0.1,0.9],[0.5,0.5],[0.4,0.6]])
john_calls.set_probability_table(cpt, [alarm, john_calls])

print john_calls.is_valid()
print alarm.is_valid()

bn.draw()
