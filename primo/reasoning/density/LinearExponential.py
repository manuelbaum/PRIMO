from primo.reasoning.density import Density
import scipy.stats
import random
import math

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
        '''This method needs some serious reworking: Variables should not be permitted
        to be parents because of their value range. Instead it should be evaluated
        if they can yield parameters for this distribution that are permitted. This 
        can in any case happen under bad influence coefficients'''
        if( not variable.get_value_range() == (0,float("Inf"))):
            raise Exception("Tried to add Variable into Gaussian densitiy, but variable had wrong value-range")
        self.b[variable]=0.0
        
    def get_probability(self,value, node_value_pairs):
        if value<=0:
            return 0
        lambda_parameter = self.b0
        for node,value in node_value_pairs:
            lambda_parameter = lambda_parameter + self.b[node]*value
        #print scipy.stats.expon(lambda_parameter).pdf(value)
        return lambda_parameter*math.exp(-lambda_parameter*value)


    def sample_global(self):
        print self.b0
        return random.expovariate(self.b0)
