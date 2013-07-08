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


bn = BayesNet()
cnf=ContinuousNodeFactory()

#create the nodes
age = cnf.createLinearExponentialNode("Age")
sun = cnf.createLinearBetaNode("Sun")
ground= cnf.createLinearGaussNode("Ground")
growth= cnf.createLinearGaussNode("Growth")
height = cnf.createLinearBetaNode("Height")
diameter = cnf.createLinearExponentialNode("Diameter")
children = cnf.createLinearExponentialNode("Children")

#add the nodes to the network
bn.add_node(age)
bn.add_node(sun)
bn.add_node(ground)
bn.add_node(growth)
bn.add_node(height)
bn.add_node(diameter)
bn.add_node(children)

#include connectivity
bn.add_edge(age,growth)
bn.add_edge(ground,growth)
bn.add_edge(sun,growth)
bn.add_edge(growth,diameter)
bn.add_edge(growth,height)
bn.add_edge(height,children)
bn.add_edge(ground,children)

#parameterization
age_parameters=LinearExponentialParameters(0.1,{})
age.set_density_parameters(age_parameters)

sun.set_density_parameters(LinearBetaParameters(2,{},2,{}))

ground.set_density_parameters(LinearGaussParameters(2.0,{},1.5))

#age,ground,sun
growth.set_density_parameters(LinearGaussParameters(0.1,{age:5.0,ground:1.0,sun:4.0},2.5))

height_parameters=LinearBetaParameters(0.1,{growth:1},0.5,{growth:0.5})
height.set_density_parameters(height_parameters)

diameter_parameters=LinearExponentialParameters(0.01,{growth:0.2})
diameter.set_density_parameters(diameter_parameters)

children.set_density_parameters(LinearExponentialParameters(0.1,{ground:1.0,height:1.0}))


mcmc_ask=MCMC(bn,1000)

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
