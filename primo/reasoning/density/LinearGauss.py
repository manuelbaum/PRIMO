# -*- coding: utf-8 -*-

from primo.reasoning.density import Density
import numpy
import scipy.stats

class LinearGauss(Density):
    '''TODO: write doc'''

    def __init__(self,variable):
        super(LinearGauss, self).__init__()
        
        self.b0=0#numpy.array([0.0])
        self.b={}
        self.var=1.0
        
    def add_variable(self, variable):
        if( not variable.get_value_range() == (-float("Inf"),float("Inf"))):
            raise Exception("Tried to add Variable into Gaussian densitiy, but variable had wrong value-range")
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
        
    def sample(self):
        return numpy.random.multivariate_normal(self.b0,self.var)
        
    
            
