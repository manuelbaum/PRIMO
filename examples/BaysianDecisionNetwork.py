from primo.networks import BayesianDecisionNetwork
from primo.nodes import DecisionNode
from primo.nodes import UtilityNode
from primo.nodes import DiscreteNode
from primo.inference.decision import MakeDecision

import numpy

'''Example of a Bayesian Decision Network found in 
Barber, David - Bayesian Reasoning and Machine Learning
Page 111ff
'''

bdn = BayesianDecisionNetwork()

education = DecisionNode("education", ["do Phd", "no Phd"])
cost = UtilityNode("cost")
prize = DiscreteNode("prize", ["prize", "no prize"])
income = DiscreteNode("income", ["low", "average", "high"])
benefit = UtilityNode("benefit")
startup = DecisionNode("startUp", ["do startUp", "no startUp"])
costStartup = UtilityNode("costStartup")

#bdn.add_node(startup)
bdn.add_node(education)
bdn.add_node(cost)
bdn.add_node(prize)
bdn.add_node(income)
bdn.add_node(benefit)
bdn.add_node(startup)
bdn.add_node(costStartup)

bdn.add_edge(education, cost)
bdn.add_edge(education, prize)
bdn.add_edge(prize, startup)
bdn.add_edge(startup, income)
bdn.add_edge(startup, costStartup)
bdn.add_edge(prize, income)
bdn.add_edge(income, benefit)

costut=numpy.array([-50000, 0])
cost.set_utility_table(costut, [education])

benefitut=numpy.array([100000,200000,500000])
benefit.set_utility_table(benefitut,[income])

startuput=numpy.array([-20000,0])
costStartup.set_utility_table(startuput,[startup])

income.set_probability(0.1,[(income,"low"),(startup,"do startUp"), (prize,"no prize")])
income.set_probability(0.2,[(income,"low"),(startup,"no startUp"), (prize,"no prize")])
income.set_probability(0.005,[(income,"low"),(startup,"do startUp"), (prize,"prize")])
income.set_probability(0.005,[(income,"low"),(startup,"no startUp"), (prize,"prize")])
income.set_probability(0.5,[(income,"average"),(startup,"do startUp"), (prize,"no prize")])
income.set_probability(0.6,[(income,"average"),(startup,"no startUp"), (prize,"no prize")])
income.set_probability(0.005,[(income,"average"),(startup,"do startUp"), (prize,"prize")])
income.set_probability(0.015,[(income,"average"),(startup,"no startUp"), (prize,"prize")])
income.set_probability(0.4,[(income,"high"),(startup,"do startUp"), (prize,"no prize")])
income.set_probability(0.2,[(income,"high"),(startup,"no startUp"), (prize,"no prize")])
income.set_probability(0.99,[(income,"high"),(startup,"do startUp"), (prize,"prize")])
income.set_probability(0.8,[(income,"high"),(startup,"no startUp"), (prize,"prize")])

prize.set_probability(0.0000001,[(prize,"prize"),(education,"no Phd")])
prize.set_probability(0.001,[(prize,"prize"),(education,"do Phd")])
prize.set_probability(0.9999999,[(prize,"no prize"),(education,"no Phd")])
prize.set_probability(0.999,[(prize,"no prize"),(education,"do Phd")])

bdn.set_partialOrdering([education, [prize], startup, [income]])

print "make decision"
md = MakeDecision(bdn)
decision = md.max_sum(education)

education.set_state(decision[1])
print decision
start=md.max_sum(startup)
print start
startup.set_state(start[1])

bdn.draw()