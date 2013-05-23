# -*- coding: utf-8 -*-

from primo.reasoning.density import Density
import numpy

class Gauss(Density):
    '''TODO: write doc'''

    def __init__(self,variable):
        super(Gauss, self).__init__()
        
        self.mu=numpy.array([0.0])
        self.C=numpy.array([[1.0]])
        
    def add_variable(self, variable):
        if( not variable.get_value_range() == (-float("Inf"),float("Inf"))):
            raise Exception("Tried to add Variable into Gaussian densitiy, but variable had wrong value-range")
        
        numpy.append(self.mu,[0])
        (m,n)=self.C.shape
        self.C.resize((m+1,n+1))
        self.C[m,n]=1.0
        
    def set_mu(self, mu):
        self.mu=mu
        
    def set_cov(self, C):
        self.C=C
        
    def sample(self):
        return numpy.random.multivariate_normal(self.mu,self.C)
            
