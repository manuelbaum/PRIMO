# -*- coding: utf-8 -*-

from primo.reasoning.density import Density
from primo.reasoning.ContinuousNode import ContinuousNode
import numpy
import scipy.stats
import random

class GaussParameters(object):
    '''
    This represents the parameters for the Gauss-density class.
    '''
    def __init__(self, b0,b,var):
        #offset for the mean of this variable, a priori
        self.b0=b0
        #a vector that holds one weight for each variable that this density depends on
        self.b=b
        #the variance
        self.var=var

class Gauss(Density):
    '''
    This class represents a one-dimensional normal distribution with a mean that
    depends linear on the parents but with invariant variance.'''

    def __init__(self,variable):
        super(Gauss, self).__init__()
        
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
        
    def sample_global(self,state,lower_limit,upper_limit):
        '''This method can be used to sample from this distribution. It is necessary that 
        a value for each parent is specified and it is possible to constrain the
        value that is being sampled to some intervall.
        @param state: A dict (node->value) that specifies a value for each variable
            that this density depends on.
        @param lower_limit: The lower limit of the interval that is allowed to be
            sampled as value.
        @param upper_limit: The upper limit of the interval that is allowed to be
            sampled as value.
        @returns: The sampled value. A real number.
        '''
        
        distribution=scipy.stats.norm(self._compute_offset_given_parents(state), self.var**0.5)
        
        lower_cdf=distribution.cdf(lower_limit)
        upper_cdf=distribution.cdf(upper_limit)
        
        sample_in_integral=random.uniform(lower_cdf, upper_cdf)
        
        sample=distribution.ppf(sample_in_integral)
    
    
        return sample
            
