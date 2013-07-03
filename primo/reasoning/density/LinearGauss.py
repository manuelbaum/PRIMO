# -*- coding: utf-8 -*-

from primo.reasoning.density import Density
from primo.reasoning.ContinuousNode import ContinuousNode
import numpy
import scipy.stats
import random

class LinearGaussParameters(object):
    def __init__(self, b0,b,var):
        self.b0=b0
        self.b=b
        self.var=var

class LinearGauss(Density):
    '''TODO: write doc'''

    def __init__(self,variable):
        super(LinearGauss, self).__init__()
        
        self.b0=0#numpy.array([0.0])
        self.b={}
        self.var=1.0
        
    def set_parameters(self,parameters):
        self.set_b0(parameters.b0)
        self.set_b(parameters.b)
        self.set_var(parameters.var)
        
    def add_variable(self, variable):

        if not isinstance(variable, ContinuousNode):
            raise Exception("Tried to add Variable into Gaussian densitiy, but variable is not continuous")
        self.b[variable]=0.0
    

    def get_probability(self, x, node_value_pairs):
        
        reduced_mu = self.b0
        for node,value in node_value_pairs:
            reduced_mu = reduced_mu + self.b[node]*value
        return scipy.stats.norm(reduced_mu, numpy.sqrt(self.var)).pdf(x)
        
        
    def set_b(self, variable, b):
        if not variable in b.keys():
            raise Exception("Tried to set dependency-variable b for a variable that has not yet been added to this variable's dependencies")
        self.b[variable]=b
        
    def set_b(self, b):
        if not set(self.b.keys())==set(b.keys()):
            raise Exception("The variables given in the new b do not match the old dependencies of this density")
        self.b=b
        
    def set_b0(self, b0):
        self.b0=b0
        
    def set_var(self, var):
        self.var=var
        
    def _compute_offset_given_parents(self, state):
        x = self.b0
        for node in self.b.keys():
            if node in state.keys():
                x = x + self.b[node]*state[node]
        return x
        
    def sample_global(self,state):
        return random.normalvariate(self._compute_offset_given_parents(state),self.var**0.5)
            
