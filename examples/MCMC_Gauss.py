from primo.core import BayesNet
from primo.reasoning import ContinuousNodeFactory
from primo.reasoning.density import LinearGaussParameters
from primo.reasoning.density import Gauss
from primo.reasoning import MCMC
from primo.reasoning import EvidenceEqual as EvEq
from primo.reasoning import EvidenceLower as EvLower
from primo.reasoning import EvidenceIntervall as EvInterval

import numpy

#Construct some simple BayesianNetwork. In this example it models
#the linear relationship between the age of a plant and the height that
#it has grown up to (+noise)

#topology
bn = BayesNet()
cnf=ContinuousNodeFactory()
age = cnf.createLinearGaussNode("Plant_age")
height = cnf.createLinearGaussNode("Plant_height")
diameter = cnf.createLinearGaussNode("Plant_diameter")
bn.add_node(age)
bn.add_node(height)
bn.add_node(diameter)
bn.add_edge(age,height)
bn.add_edge(age,diameter)




#parameterization
age_b0=4.0
age_var=2.0
age_b={}
age_parameters=LinearGaussParameters(age_b0,age_b,age_var)
age.set_density_parameters(age_parameters)

height_b0=2.0
height_var=1.5
height_b={age:0.5}
height_parameters=LinearGaussParameters(height_b0,height_b,height_var)
height.set_density_parameters(height_parameters)

diameter_parameters=LinearGaussParameters(0.1,{age:-0.2},0.1)
diameter.set_density_parameters(diameter_parameters)


mcmc_ask=MCMC(bn,1000)

evidence={age:EvEq(2)}


#print "ProbabilityOfEvidence: " 
#poe=mcmc_ask.calculate_PoE(evidence)
#print poe

print "PosteriorMarginal:"
pm=mcmc_ask.calculate_PosteriorMarginal([height,diameter],evidence,Gauss)
print pm

print "PriorMarginal:"
pm=mcmc_ask.calculate_PriorMarginal([height,diameter],Gauss)
print pm

print "ProbabilityOfEvidence:"
poe=mcmc_ask.calculate_PoE({age:EvLower(4.0)})
print "p(age<4.0):"+str(poe)+ " GroundTruth:0.5"
poe=mcmc_ask.calculate_PoE({age:EvInterval(4.0-2.0**0.5,4.0)})
print "p(4.0-2.0^0.5<age<4.0):"+str(poe)+ " GroundTruth:1/3"
#print "PriorMarginal:"
#pm=mcmc_ask.calculate_PriorMarginal([alarm])
#print "Alarm: " + str(pm)
#pm=mcmc_ask.calculate_PriorMarginal([burglary])
#print "Burglary: " + str(pm)
