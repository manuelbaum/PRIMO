# -*- coding: utf-8 -*-

from primo.reasoning.density import Density
import numpy

class LinearGauss(Density):
    '''TODO: write doc'''

    def __init__(self,variable):
        super(LinearGauss, self).__init__()
        
        self.b0=numpy.array([0.0])
        self.b=None
        self.var=numpy.array([[1.0]])
        
    def add_variable(self, variable):
        if( not variable.get_value_range() == (-float("Inf"),float("Inf"))):
            raise Exception("Tried to add Variable into Gaussian densitiy, but variable had wrong value-range")
        
        numpy.append(self.b0,[0])
        (m,n)=self.var.shape
        self.var.resize((m+1,n+1))
        self.var[m,n]=1.0
        
    def set_b(self, b):
        self.b=b
        
    def set_b0(self, b0):
        self.b0=b0
        
    def set_var(self, var):
        self.var=var
        
    def sample(self):
        return numpy.random.multivariate_normal(self.b0,self.var)
        
    
            
