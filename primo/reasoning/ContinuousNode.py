from primo.core import Node
import random

class ContinuousNode(Node):
    def __init__(self, name, value_range, DensityClass):
        super(ContinuousNode, self).__init__(name)
        
        self.value_range = value_range
        self.density_class = DensityClass
        self.cpd = DensityClass(self)
        
    def set_density_parameters(self, density_parameters):
        self.cpd.set_parameters(density_parameters)
        
    def sample_uniform(self):
        sampled_value = random.uniform(self.value_range[0],self.value_range[1])
        return sampled_value
        
    def sample_proposal(self, x=None):
        return self.cpd.sample_proposal(x)
        
    def get_probability(self, value, node_value_pairs):
        return self.cpd.get_probability(value, node_value_pairs)
        
