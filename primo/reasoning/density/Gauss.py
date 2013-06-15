# -*- coding: utf-8 -*-

from primo.reasoning.density import Density
import numpy

class Gauss(Density):
    '''TODO: write doc'''

    def __init__(self):
        super(Gauss, self).__init__()
        
        self.mu=numpy.array([0.0])
        self.C=numpy.array([[1.0]])
        self.variables=[]
        print self.mu
        print self.C
        
    def add_variable(self, variable):
        if( not variable.get_value_range() == (-float("Inf"),float("Inf"))):
            raise Exception("Tried to add Variable into Gaussian densitiy, but variable had wrong value-range")
        self.variables.append(variable)
        
        
        m=len(self.variables)
        self.mu.resize([m,1])
        self.C.resize((m,m))
        
        self.C[m-1,m-1]=1.0
        
    def set_mu(self, mu):
        self.mu=mu
        
    def set_cov(self, C):
        self.C=C
        
    def sample(self):
        return numpy.random.multivariate_normal(self.mu,self.C)
            
            
    def parametrize_from_states(self, samples, number_of_samples):
        '''This method uses a list of variable-instantiations to change this node's parametrization
         to represent a Gaussian constructed from the given samples.
            The Argument samples is a list of pairs (RandomNode, value).'''
            
        X=numpy.empty((number_of_samples, len(self.variables)))
        for i,state in enumerate(samples):
            for j,variable in enumerate(self.variables):
                X[i,j]=state[variable]

        self.mu=numpy.mean(X)
        self.C=numpy.cov(X.transpose())
        
        print X
        print "--mu--"
        print self.mu
        print "--C--"
        print self.C
