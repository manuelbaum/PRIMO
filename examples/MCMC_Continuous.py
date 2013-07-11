from primo.core import BayesNet
from primo.reasoning import ContinuousNodeFactory
from primo.reasoning.density import LinearExponentialParameters
from primo.reasoning.density import LinearBetaParameters
from primo.reasoning.density import LinearGaussParameters
from primo.reasoning.density import Gauss
from primo.reasoning import MCMC
from primo.reasoning.convergence_test import ConvergenceTestSimpleCounting

from primo.reasoning import EvidenceEqual as EvEqual
from primo.reasoning import EvidenceLower as EvLower

import numpy

#Construct some simple BayesianNetwork. 

#topology
bn = BayesNet()
cnf=ContinuousNodeFactory()
age = cnf.createLinearExponentialNode("Plant_age")
height = cnf.createLinearGaussNode("Plant_height")
diameter = cnf.createLinearBetaNode("Plant_diameter")
bn.add_node(age)
bn.add_node(height)
bn.add_node(diameter)
bn.add_edge(age,height)
bn.add_edge(age,diameter)

#parameterization
#Semantics: Many young plants and the higher the age the lower the probabilty
#->lambda=2.0
age_parameters=LinearExponentialParameters(0.0,{})
age.set_density_parameters(age_parameters)

#Semantics: plants start at 0.1 meters underground and grow each year by 1 meter.
#           variance is 0.3 
height_parameters=LinearGaussParameters(-0.1,{age:1},0.3)
height.set_density_parameters(height_parameters)

#Semantics: At small age: low alpha, high beta -> skew to the left: thin plants
#            At higher age: high alpha, low beta -> skew to the right: thick plants
diameter_parameters=LinearBetaParameters(-10.0,{age:4.0},10.0,{age:-4.0})
diameter.set_density_parameters(diameter_parameters)


mcmc_ask=MCMC(bn,1000,convergence_test=ConvergenceTestSimpleCounting(500))


print "------PriorMarginal:------"


pm=mcmc_ask.calculate_PriorMarginal([age],Gauss)
print pm
print "Ground truth: mu=0.5 C=[0.25]"
pm=mcmc_ask.calculate_PriorMarginal([height],Gauss)
print pm
print ""


print "------PosteriorMarginal:------"
pm=mcmc_ask.calculate_PosteriorMarginal([age,height],{age:EvEqual(2)},Gauss)
print "P(age,height|age=2):"
print pm
print "Ground truth: age=2, height=mu:1.9,C=0.3"
print ""

pm=mcmc_ask.calculate_PosteriorMarginal([age,height],{age:EvLower(0.1)},Gauss)
print "P(age,height|age<0.1):"
print pm
print "Ground truth: age=0:0.1, height=mu:-0.1:0.0,C=0.3"
print ""

print "------PropabilityOfEvidence------"
poe=mcmc_ask.calculate_PoE({age:EvLower(0.347)})
print "Probabilty that age is lower than it's median:"
print "p(age<0.347)="+str(poe)
print "Ground truth=0.5"
print ""

print "------MAP------"
map_hypothesis=mcmc_ask.calculate_MAP([height,diameter],{},Gauss)
print map_hypothesis



