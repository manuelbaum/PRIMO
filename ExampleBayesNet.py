from  core.BayesNet import *
from  reasoning.DiscreteNode import DiscreteNode

bn = BayesNet()
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


bn.draw()
