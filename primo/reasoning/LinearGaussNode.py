# -*- coding: utf-8 -*-

from primo.reasoning import RandomNode
from primo.reasoning.density import LinearGauss
import random

class LinearGaussNode(RandomNode):
    '''TODO: write doc'''

    def __init__(self, name):
        super(LinearGaussNode, self).__init__(name)
        
        self.value_range = (-float("Inf"),float("Inf"))
        self.cpd = LinearGauss(self)
        

    def set_density_parameters(self, b0, b, var):
        self.cpd.set_b0(b0)
        self.cpd.set_b(b)
        self.cpd.set_var(var)
        
    def get_probability(self, value, node_value_pairs):
        return self.cpd.get_probability(value, node_value_pairs)

    def announce_parent(self, node):
        self.cpd.add_variable(node)

    def __str__(self):
        return self.name # + "\n" + str(self.cpd)

    def get_cpd_reduced(self, evidence):
        return self.cpd.reduction(evidence)

    def get_value_range(self):
        return self.value_range
        
    def set_cpd(self, cpd):
        self.cpd = cpd
        
    def get_cpd(self):
        return self.cpd
        
    def sample_uniform(self):
        sampled_value = random.uniform(self.value_range[0],self.value_range[1])
        return sampled_value
        
    def sample_proposal(self, x=0.0):
        return random.normalvariate(x,1.0)

    def is_valid(self):
        raise Exception("Called unimplemented Function: GaussNode.is_valid()")
