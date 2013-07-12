from primo.reasoning.density import Density
import scipy.stats
import random
import math
from primo.reasoning import ContinuousNode

class ExponentialParameters(object):
    '''
    This represents the parameters for the Exponential-density class.
    '''
    def __init__(self, b0, b):
        #lambda a-priori
        self.b0=b0
        #a dict (node,coefficient) that holds the weights that define the depency on each node
        self.b=b

        

class Exponential(Density):
    '''
    This class represents an exponential probabilty density. Unfortunately this
    is currently a little bulky to use as the parameters for the dependency are
    not very transparent. This is how the dependency works:
    
    The parameter lambda for the exponential distribution is computed analogous
    as the activation of a perceptron with sigmoid-activation function:
    output_scale * sigmoid(input_scale* (b0 + b'state)) where b'state means the dot product between b (a vector
    of weights) and state (a vector with a value for each variable that this
    density depends on). Here: sigmoid=1/(1+exp(-x))
    The parameters output_scale and input_scale can be used to strech or compress
    the sigmoid.
    
    The reason for this is that the parameter lambda is required to be >0. And with
    linear dependencies on the parents this could in no way be guaranteed.
    
    Why the sigmoid function:
    I had to guarantee that the parameter lambda is > 0. As i did not want to
    impose any restrictions on the value range of the parents it was necessary
    to map the support of the parents values to a valid support for lambda. In
    other (and maybe more correct words): The dependency function to compute
    lambda needed to be of the form R^n->]0,inf].
    
    The first function that came to my mind was:
    weighted sum of the parents values put into an exponential function. This
    caused problems due to the fast growth of the exponential.
    For that reason i switched to the sigmoid function that guarantees 0<lambda<1.
    And because lambda<1 is not very practical output_scale has been introduced
    to scale from ]0,1[ to ]0,output_scale[. 
    
    input_scale can be used to strech the sigmoid in input_direction.
    '''
    def __init__(self, node):
        #the coefficients for the weighted sum of parent-values
        self.b={}
        #bias
        self.b0=0
        #the node that this density is associated with
        self.node=node
        #scaling coefficient to stretch or compress the sigmoid in input-direction
        self.input_scale=1.0
        #scaling coefficient to stretch or compress the sigmoid in output-direction
        self.output_scale=4.0
        
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
        _lambda = self._compute_lambda_given_parents(dict(node_value_pairs))
        #Evaluate the displaced density at value
        return _lambda*math.exp(-_lambda*value)

    def _compute_lambda_given_parents(self, state):
        x = self.b0
        for node in self.b.keys():
            if node in state.keys():
                x = x + self.b[node]*state[node]
        _lambda=self.output_scale*1.0/(1.0+math.exp(-x*self.input_scale))
        return _lambda

    def sample_global(self,state, lower_limit, upper_limit):
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
        _lambda=self._compute_lambda_given_parents(state)
        distribution=scipy.stats.expon(loc=0,scale=1.0/_lambda)
        
        lower_cdf=distribution.cdf(lower_limit)
        upper_cdf=distribution.cdf(upper_limit)
        
        sample_in_integral=random.uniform(lower_cdf, upper_cdf)
        
        sample=distribution.ppf(sample_in_integral)
        
        #sample=random.expovariate(_lambda)
        #print "EXPO-SAMPLE: "+str(sample)+" at lambda: "+str(_lambda)
        return sample
