from primo.reasoning.density import Density
import scipy.stats
import random
import math
from primo.reasoning import ContinuousNode

class LinearExponentialParameters(object):
    def __init__(self, b0, b):
        self.b0=b0
        self.b=b

        

class LinearExponential(Density):
    def __init__(self, node):
        self.b={}
        self.b0=0
        self.node=node
        
    def set_parameters(self,parameters):
        self.b=parameters.b
        self.b0=parameters.b0
        
    def add_variable(self, variable):
        '''This method needs some serious reworking: Variables should not be denied
        to be parents because of their value range. Instead it should be evaluated
        if they can yield parameters for this distribution that are permitted. This 
        can in any case happen under bad influence coefficients'''
        if( not isinstance(variable,ContinuousNode.ContinuousNode)):
            raise Exception("Tried to add Variable as parent, but is not a ContinuousNode")
        self.b[variable]=0.0
        
    def get_probability(self,value, node_value_pairs):
        
        #Compute the offset for the density and displace the value accordingly
        x = self.b0
        for node,value in node_value_pairs:
            x = x + self.b[node]*value
        _lambda=1.0/(1.0+math.exp(-x))
        #print "lambda:"+str(_lambda)
        #Evaluate the displaced density at value
        return _lambda*math.exp(-_lambda*value)

    def _compute_lambda_given_parents(self, state):
        x = self.b0
        for node in self.b.keys():
            if node in state.keys():
                x = x + self.b[node]*state[node]
        _lambda=1.0/(1.0+math.exp(-x))
        return _lambda

    def sample_global(self,state):
        _lambda=self._compute_lambda_given_parents(state)
        return random.expovariate(_lambda)
