import numpy

from primo.networks import BayesianNetwork
from primo.nodes import ContinuousNodeFactory

cnf = ContinuousNodeFactory()
age = cnf.createGaussNode("Plant_age")

#parameterization
age_b0=numpy.array([4])
age_variance=numpy.array([[2]])
age.set_density_parameters(age_b0,age_variance)

for i in range(8):
    print age.sample()

