from primo.core import BayesNet
from primo.reasoning import GaussNode
from primo.reasoning import MarkovChainSampler
from primo.reasoning import GibbsTransitionModel


#Construct some simple BayesianNetwork. In this example it models
#the linear relationship between the age of a plant and the height that
#it has grown up to (+noise)

#topology
bn = BayesNet()
age = GaussNode("Plant_age")
height = GaussNode("Plant_height")
bn.add_node(age)
bn.add_node(height)
bn.add_edge(age,height)

#parameterization
age_b0=numpy.array([4])
age_variance=numpy.array([2])
age_b=numpy.array()
age.set_density_parameters(age_b0,age_b,age_variance)

height_b0=numpy.array([2])
height_variance=numpy.array([1.5])
height_b=numpy.array([2])
height.set_densitiy_parameters(height_b0, height_b, height_variance)
