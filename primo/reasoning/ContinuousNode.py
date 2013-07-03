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
        
        
    def sample_local(self, x, evidence):
        '''This is the most simple and stupid implementation of the method. It
        uses bogo-search to find a sample that fits the evidence. You could
        reimplement it by constructing the integral over the normalvariate in the
        intervalls allowed by the evidence and then generate a sample directly.
        Currently this method has O(inf).'''
        v=random.normalvariate(x,1.0)
        if self in evidence.keys():
            while not evidence[self].is_compatible(v):
                v=random.normalvariate(x,1.0)
        return v
        
    def sample_global(self, state):
        '''Simple, Stupid and O(inf). Improvement idea see comment on sample_local()'''
        proposal=self.cpd.sample_global(state)
        #while not evidence.is_compatible(proposal):
        #    proposal=self.cpd.sample_global(evidence)
        return proposal
        
    def get_probability(self, value, node_value_pairs):
        return self.cpd.get_probability(value, node_value_pairs)
        
