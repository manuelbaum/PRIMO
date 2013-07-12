# -*- coding: utf-8 -*-

from primo.reasoning.density import Density
import numpy

class NDGaussParameters(object):
    def __init__(self, mu, cov):
        self.mu=mu
        self.cov=cov

class NDGauss(Density):
    '''
    This class represents an N-Dimensional gaussian density. It is currently not
    tested for inclusion into a bayesian network, but it is used to compute return
    values for inference in the continuous setting. This is not optimal yet,
    as for example, when computing the map hypothesis of a density with two or
    more modes the mean of the gaussian could be in an area of state space with
    very low probability. It would be sensible to also introduce a density
    mixture of gaussian (or similar), to account for such problems. That density
    could for example be learned with EM.
    '''

    def __init__(self):
        super(NDGauss, self).__init__()
        
        self.mu=numpy.array([0.0])
        self.C=numpy.array([[1.0]])
        self.variables=[]

        
    def add_variable(self, variable):
        v_min,v_max=variable.get_value_range()
        if not  (v_min>= -float("Inf") and v_max <=float("Inf")):
            raise Exception("Tried to add Variable into Gaussian densitiy, but variable had wrong value-range")
        self.variables.append(variable)
        
        
        m=len(self.variables)
        self.mu.resize([m,1])
        self.C.resize((m,m))
        
        self.C[m-1,m-1]=1.0
        
    def set_parameters(self,parameters):
        self.set_mu(parameters.mu)
        self.set_cov(parameters.cov)
        
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

        self.mu=numpy.mean(X,axis=0)
        self.C=numpy.cov(X.transpose())
        return self
        
    def get_most_probable_instantiation(self):
        return self.mu
        
    def __str__(self):
        ret= "Gauss(\nmu="+str(self.mu)+"\nC="+str(self.C)+")"
        return ret
