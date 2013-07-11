from primo.reasoning.density import Density
from primo.reasoning import ContinuousNode
from scipy.stats import beta
import random
import math
class LinearBetaParameters():
    def __init__(self, p0, p, q0, q):
        self.p=p
        self.q=q
        self.p0=p0
        self.q0=q0


class LinearBeta(Density):
    def __init__(self, node):
        self.p0=1
        self.q0=1
        self.p={}
        self.q={}
        self.node=node
        
        self.input_scale=0.1
        self.output_scale=5.0
        
    def set_parameters(self,parameters):
        self.p0=parameters.p0
        self.q0=parameters.q0
        self.p=parameters.p
        self.q=parameters.q
        
    def add_variable(self, variable):
        '''This method needs some serious reworking: Variables should not be permitted
        to be parents because of their value range. Instead it should be evaluated
        if they can yield parameters for this distribution that are permitted. This 
        can in any case happen under bad influence coefficients'''
        if( not isinstance(variable,ContinuousNode.ContinuousNode)):
            raise Exception("Tried to add Variable as parent, but is not a ContinuousNode")
        self.p[variable]=0.0
        self.q[variable]=0.0
        
        
    def get_probability(self,value, node_value_pairs):
        #print "Probability to compute for value:"+str(value)
        #Compute the offset for the density and displace the value accordingly
        #p = self.p0
        #q = self.q0

        #for node,node_value in node_value_pairs:
        #    p = p + self.p[node]*node_value
        #    q = q + self.q[node]*node_value
        #p=1.0/(1.0+math.exp(-p))
        #q=1.0/(1.0+math.exp(-q))
        p=self._compute_p_given_parents(dict(node_value_pairs))
        q=self._compute_q_given_parents(dict(node_value_pairs))
        #print node_value_pairs
        #print "beta "+str(p)+" "+str(q)
        probability = beta(p, q).pdf(value)
        #print "/beta"
        return probability
        
    def _compute_p_given_parents(self, state):
        x = self.p0
        for node in self.p.keys():
            if node in state.keys():
                x = x + self.p[node]*state[node]
        return self.output_scale*1.0/(1.0+math.exp(-x*self.input_scale))
        
    def _compute_q_given_parents(self, state):
        x = self.q0
        for node in self.q.keys():
            if node in state.keys():
                x = x + self.q[node]*state[node]
        return self.output_scale*1.0/(1.0+math.exp(-x*self.input_scale))


    def sample_global(self, state, lower_limit, upper_limit):
        p=self._compute_p_given_parents(state)
        q=self._compute_q_given_parents(state)
        #value=random.betavariate(p,q)
        #print "Sampled:"+str(value)
        #return value
        
        
        
        
        
        
        #_lambda=self._compute_lambda_given_parents(state)
        distribution=beta(p,q)
        
        lower_cdf=distribution.cdf(lower_limit)
        upper_cdf=distribution.cdf(upper_limit)
        
        sample_in_integral=random.uniform(lower_cdf, upper_cdf)
        
        sample=distribution.ppf(sample_in_integral)
        return sample
        
        
        
        
        
        
