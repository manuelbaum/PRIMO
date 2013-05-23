import numpy

from primo.core import BayesNet
from primo.reasoning import GaussNode

age = GaussNode("Plant_age")

#parameterization
age_b0=numpy.array([4])
age_variance=numpy.array([[2]])
age.set_density_parameters(age_b0,age_variance)

for i in range(8):
    print age.sample()

