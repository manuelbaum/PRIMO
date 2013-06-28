from primo.core import BayesNet
from primo.reasoning import ContinuousNodeFactory
from primo.reasoning.density import LinearExponentialParameters
from primo.reasoning.density import LinearBetaParameters
from primo.reasoning.density import LinearGaussParameters
from primo.reasoning.density import Gauss
from primo.reasoning import MCMC

from primo.reasoning import EvidenceEqual as EvEqual
from primo.reasoning import EvidenceIntervall as EvInterval

import numpy

#Construct some simple BayesianNetwork. In this example it models
#the linear relationship between the age of a plant and the height that
#it has grown up to (+noise)

#topology
bn = BayesNet()
cnf=ContinuousNodeFactory()
age = cnf.createLinearExponentialNode("Plant_age")
height = cnf.createLinearGaussNode("Plant_height")
#diameter = cnf.createLinearBetaNode("Plant_diameter")
bn.add_node(age)
bn.add_node(height)
#bn.add_node(diameter)
bn.add_edge(age,height)
#bn.add_edge(age,diameter)

#parameterization
age_parameters=LinearExponentialParameters(4,{})
age.set_density_parameters(age_parameters)

height_parameters=LinearGaussParameters(0.1,{age:1},0.3)
height.set_density_parameters(height_parameters)

#diameter_parameters=LinearGaussParameters(0.1,{age:-0.2},0.1)
#diameter.set_density_parameters(diameter_parameters)


mcmc_ask=MCMC(bn)

evidence={age:EvEqual(2)}


#print "ProbabilityOfEvidence: " 
#poe=mcmc_ask.calculate_PoE(evidence)
#print poe

print "PosteriorMarginal:"
pm=mcmc_ask.calculate_PosteriorMarginal([age,height],evidence,Gauss)
#pm=mcmc_ask.calculate_PosteriorMarginal([height],evidence,Gauss)
print pm

print "PriorMarginal:"
pm=mcmc_ask.calculate_PriorMarginal([age],Gauss)
print pm
#pm=mcmc_ask.calculate_PriorMarginal([height,diameter],Gauss)
pm=mcmc_ask.calculate_PriorMarginal([height],Gauss)
print pm
