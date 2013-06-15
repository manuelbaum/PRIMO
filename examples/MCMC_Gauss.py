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
bn.add_node(age)
bn.add_node(height)
bn.add_edge(age,height)

#parameterization
age_b0=4.0
age_var=2.0
age_b={}
age.set_density_parameters(age_b0,age_b,age_var)
#age.set_density_parameters(age_b0,age_variance)

height_b0=2.0
height_var=1.5
height_b={age:0.5}
height.set_density_parameters(height_b0, height_b, height_var)
#height.set_density_parameters(height_b0, height_variance)


mcmc_ask=MCMC(bn)

evidence={age:2}


#print "ProbabilityOfEvidence: " 
#poe=mcmc_ask.calculate_PoE(evidence)
#print poe

print "PosteriorMarginal:"
pm=mcmc_ask.calculate_PosteriorMarginal([height],evidence,Gauss)
print pm

#print "PriorMarginal:"
#pm=mcmc_ask.calculate_PriorMarginal([alarm])
#print "Alarm: " + str(pm)
#pm=mcmc_ask.calculate_PriorMarginal([burglary])
#print "Burglary: " + str(pm)
