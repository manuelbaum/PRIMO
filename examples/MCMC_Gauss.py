from primo.core import BayesNet
from primo.reasoning import LinearGaussNode
from primo.reasoning.density import Gauss
from primo.reasoning import MCMC

import numpy

#Construct some simple BayesianNetwork. In this example it models
#the linear relationship between the age of a plant and the height that
#it has grown up to (+noise)

#topology
bn = BayesNet()
age = LinearGaussNode("Plant_age")
height = LinearGaussNode("Plant_height")
diameter = LinearGaussNode("Plant_diameter")
bn.add_node(age)
bn.add_node(height)
bn.add_node(diameter)
bn.add_edge(age,height)
bn.add_edge(age,diameter)

#parameterization
age_b0=4.0
age_var=2.0
age_b={}
age.set_density_parameters(age_b0,age_b,age_var)

height_b0=2.0
height_var=1.5
height_b={age:0.5}
height.set_density_parameters(height_b0, height_b, height_var)

diameter_b0=0.1
diameter_var=0.1
diameter_b={age:-0.2}
diameter.set_density_parameters(diameter_b0, diameter_b, diameter_var)


mcmc_ask=MCMC(bn)

evidence={age:2}


#print "ProbabilityOfEvidence: " 
#poe=mcmc_ask.calculate_PoE(evidence)
#print poe

print "PosteriorMarginal:"
pm=mcmc_ask.calculate_PosteriorMarginal([height,diameter],evidence,Gauss)
print pm

print "PriorMarginal:"
pm=mcmc_ask.calculate_PriorMarginal([height,diameter],Gauss)
print pm

#print "PriorMarginal:"
#pm=mcmc_ask.calculate_PriorMarginal([alarm])
#print "Alarm: " + str(pm)
#pm=mcmc_ask.calculate_PriorMarginal([burglary])
#print "Burglary: " + str(pm)
