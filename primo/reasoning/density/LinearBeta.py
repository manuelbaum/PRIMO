from primo.reasoning.density import Density
from scipy.stats import beta
import random

class LinearBetaParameters():
    def __init__(self, b0, b, alpha, beta):
        self.b0=b0
        self.b=b
        self.alpha=alpha
        self.beta=beta

class LinearBeta(Density):
    def __init__(self, node):
        self.b={}
        self.b0=0
        self.alpha=1
        self.beta=1
        self.node=node
        
    def set_parameters(self,parameters):
        self.b=parameters.b
        self.b0=parameters.b0
        self.alpha=parameters.alpha
        self.beta=parameters.beta
        
    def add_variable(self, variable):
        '''This method needs some serious reworking: Variables should not be permitted
        to be parents because of their value range. Instead it should be evaluated
        if they can yield parameters for this distribution that are permitted. This 
        can in any case happen under bad influence coefficients'''
        if( not variable.get_value_range() == (0,float("Inf"))):
            raise Exception("Tried to add Variable into Gaussian densitiy, but variable had wrong value-range")
        self.b[variable]=0.0
        
    def get_probability(self,value, node_value_pairs):
        #print "Probability to compute for value:"+str(value)
        #Compute the offset for the density and displace the value accordingly
        x = self.b0
        #print "X:"+str(x)
        for node,node_value in node_value_pairs:
            x = x + self.b[node]*node_value
            #print "X:"+str(x)
        #print value
        value=value-x
        #Evaluate the displaced density at value
        #print str(value)
        if value<0 or value>1:
            return 0
        return beta(self.alpha, self.beta).pdf(value)
        
    def _compute_offset_given_parents(self, state):
        x = self.b0
        for node in self.b.keys():
            if node in state.keys():
                x = x + self.b[node]*state[node]
        return x


    def sample_global(self, state):
        value=random.betavariate(self.alpha,self.beta)+self._compute_offset_given_parents(state)
        #print "Sampled:"+str(value)
        return value
