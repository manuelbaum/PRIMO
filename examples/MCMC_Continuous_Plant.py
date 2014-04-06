from primo.networks import BayesianNetwork
from primo.nodes import ContinuousNodeFactory
from primo.densities import ExponentialParameters
from primo.densities import BetaParameters
from primo.densities import GaussParameters
from primo.densities import NDGauss
from primo.inference.mcmc import MCMC

from primo.evidence import EvidenceEqual as EvEqual
from primo.evidence import EvidenceInterval as EvInterval

import numpy

#Construct some simple BayesianNetwork. In this example it models
#the linear relationship between the age of a plant and the height that
#it has grown up to (+noise)


bn = BayesianNetwork()
cnf=ContinuousNodeFactory()

#create the nodes
age = cnf.createExponentialNode("Age")
sun = cnf.createBetaNode("Sun")
ground= cnf.createGaussNode("Ground")
growth= cnf.createGaussNode("Growth")
height = cnf.createBetaNode("Height")
diameter = cnf.createExponentialNode("Diameter")
children = cnf.createExponentialNode("Children")

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
age.set_density_parameters(ExponentialParameters(0.1,{}))

sun.set_density_parameters(BetaParameters(2,{},2,{}))

ground.set_density_parameters(GaussParameters(2.0,{},1.5))

growth.set_density_parameters(GaussParameters(0.1,{age:5.0,ground:1.0,sun:4.0},2.5))

height.set_density_parameters(BetaParameters(0.1,{growth:1},0.5,{growth:0.5}))

diameter.set_density_parameters(ExponentialParameters(0.01,{growth:0.2}))

children.set_density_parameters(ExponentialParameters(0.1,{ground:1.0,height:1.0}))


mcmc_ask=MCMC(bn,1000)

evidence={age:EvEqual(2)}


print "PosteriorMarginal:"
pm=mcmc_ask.calculate_PosteriorMarginal([age,height],evidence,NDGauss)
#pm=mcmc_ask.calculate_PosteriorMarginal([height],evidence,Gauss)
print pm

print "PriorMarginal:"
pm=mcmc_ask.calculate_PriorMarginal([age],NDGauss)
print pm
#pm=mcmc_ask.calculate_PriorMarginal([height,diameter],Gauss)
pm=mcmc_ask.calculate_PriorMarginal([height],NDGauss)
print pm
