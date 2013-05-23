# -*- coding: utf-8 -*-

from primo.reasoning import RandomNode
from primo.reasoning.density import Gauss


class GaussNode(RandomNode):
    '''TODO: write doc'''

    def __init__(self, name):
        super(GaussNode, self).__init__(name)
        
        self.value_range = (-float("Inf"),float("Inf"))
        self.cpd = Gauss(self)
        

    def set_density_parameters(self,mu, cov):
        self.cpd.set_mu(mu)
        self.cpd.set_cov(cov)

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
        
    def sample(self):
        return self.cpd.sample()

    def is_valid(self):
        raise Exception("Called unimplemented Function: GaussNode.is_valid()")
