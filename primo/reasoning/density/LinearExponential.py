from primo.reasoning.density import Density
import scipy.stats
import random
import math

class LinearExponentialParameters(object):
    def __init__(self, b0, b, lambda0):
        self.b0=b0
        self.b=b
        self.lambda0=lambda0

        

class LinearExponential(Density):
    def __init__(self, node):
        self.b={}
        self.b0=0
        self.lambda0=1
        self.node=node
        
    def set_parameters(self,parameters):
        self.b=parameters.b
        self.b0=parameters.b0
        self.lambda0=parameters.lambda0
        
    def add_variable(self, variable):
        '''This method needs some serious reworking: Variables should not be denied
        to be parents because of their value range. Instead it should be evaluated
        if they can yield parameters for this distribution that are permitted. This 
        can in any case happen under bad influence coefficients'''
        if( not variable.get_value_range() == (0,float("Inf"))):
            raise Exception("Tried to add Variable into Gaussian densitiy, but variable had wrong value-range")
        self.b[variable]=0.0
        
    def get_probability(self,value, node_value_pairs):
        
        #Compute the offset for the density and displace the value accordingly
        x = self.b0
        for node,value in node_value_pairs:
            x = x + self.b[node]*value
        value=value-x
        #Evaluate the displaced density at value
        if value<0:
            return 0
        return self.lambda0*math.exp(-self.lambda0*value)

    def _compute_offset_given_parents(self, state):
        x = self.b0
        for node in self.b.keys():
            if node in state.keys():
                x = x + self.b[node]*state[node]
        return x

    def sample_global(self,state):
        return random.expovariate(self.lambda0)+self._compute_offset_given_parents(state)
