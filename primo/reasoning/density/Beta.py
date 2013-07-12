from primo.reasoning.density import Density
from primo.reasoning import ContinuousNode
from scipy.stats import beta
import random
import math
class BetaParameters():
    '''
    This represents the parameters for the beta-density class.
    '''
    def __init__(self, p0, p, q0, q):
        #vector of coefficients for parent values to compute p
        self.p=p
        #vector of coefficients for parent values to compute q
        self.q=q
        #bias for p
        self.p0=p0
        #bias for q
        self.q0=q0


class Beta(Density):
    '''
    This class represents an beta probabilty density. Unfortunately this
    is currently a little bulky to use as the parameters for the dependency are
    not very transparent. This is how the dependency works:
    
    The parameters p,q for the exponential distribution are computed analogous
    as the activation of a perceptron with sigmoid-activation function:
    output_scale * sigmoid(input_scale* (b0 + b'state)) where b'state means the dot product between b (a vector
    of weights) and state (a vector with a value for each variable that this
    density depends on). Here: sigmoid=1/(1+exp(-x))
    The parameters output_scale and input_scale can be used to strech or compress
    the sigmoid.
    
    The reason for this is that the parameters are required to be >0. And with
    linear dependencies on the parents this could in no way be guaranteed.
    
    Why the sigmoid function:
    I had to guarantee that the parameters are > 0. As i did not want to
    impose any restrictions on the value range of the parents it was necessary
    to map the support of the parents values to a valid support for the parameters. In
    other (and maybe more correct words): The dependency function to compute
    p and q needed to be of the form R^n->]0,inf].
    
    The first function that came to my mind was:
    weighted sum of the parents values put into an exponential function. This
    caused problems due to the fast growth of the exponential.
    For that reason i switched to the sigmoid function that guarantees 0<p,q<1.
    And because p,q<1 is not very practical output_scale has been introduced
    to scale from ]0,1[ to ]0,output_scale[. 
    
    input_scale can be used to strech the sigmoid in input_direction.
    '''
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
        if( not isinstance(variable,ContinuousNode.ContinuousNode)):
            raise Exception("Tried to add Variable as parent, but is not a ContinuousNode")
        self.p[variable]=0.0
        self.q[variable]=0.0
        
        
    def get_probability(self,value, node_value_pairs):
        p=self._compute_p_given_parents(dict(node_value_pairs))
        q=self._compute_q_given_parents(dict(node_value_pairs))
        probability = beta(p, q).pdf(value)

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
        p=self._compute_p_given_parents(state)
        q=self._compute_q_given_parents(state)

        distribution=beta(p,q)
        
        lower_cdf=distribution.cdf(lower_limit)
        upper_cdf=distribution.cdf(upper_limit)
        
        sample_in_integral=random.uniform(lower_cdf, upper_cdf)
        
        sample=distribution.ppf(sample_in_integral)
        return sample
        
        
        
        
        
        
