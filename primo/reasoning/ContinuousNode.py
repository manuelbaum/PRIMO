# -*- coding: utf-8 -*-

from primo.reasoning import RandomNode
import random

class ContinuousNode(RandomNode):
    '''
    Represents a random-variable with a real-valued domain. Can only be defined
    on a subset or on whole R. The probability density can have different forms.
    Objects of this class can be created by a ContinuousNodeFactory.
    '''
    def __init__(self, name, value_range, DensityClass):
        super(ContinuousNode, self).__init__(name)
        
        #value_range is a 2-tuple that defines this variable's domain.
        self.value_range = value_range
        #the class density_class defines the class of function that is used
        #for this ContinuousNode's pdf.
        self.density_class = DensityClass
        #cpd - ConditionalProbabilityDensity is the concrete density function 
        #of this ContinuousNode, conditioned on this Node's parents.
        self.cpd = DensityClass(self)
        
    def __str__(self):
        return self.name
        
    def set_density_parameters(self, density_parameters):
        self.cpd.set_parameters(density_parameters)
        
#    def sample_uniform(self):
#        sampled_value = random.uniform(self.value_range[0],self.value_range[1])
#        return sampled_value
#        
#    def sample_proposal(self, x=None):
#        return self.cpd.sample_proposal(x)
        
        
    def sample_local(self, x, evidence):
        '''
        This method can be used to do a random walk in the domain of this node.
        
        @param x: The spot around which the next sample shall be generated.
        @param evidence: Evidence which is to be concerned when new samples are
            being generated. I am not entirely sure that this belongs here or is
            correct in theory...
        
        ATTENTION:
        This is the most simple and stupid implementation of the method. It
        uses bogo-search to find a sample that fits the evidence. You could
        reimplement it by constructing the integral over the normalvariate in the
        intervalls allowed by the evidence and then generate a sample directly.
        Currently this method has O(inf).'''
        v=random.normalvariate(x,1.0)
        if self in evidence.keys():
            while not evidence[self].is_compatible(v):
                v=random.normalvariate(x,1.0)
        return v
        
    def sample_global(self, state):
        '''
        This method can be used to sample from this local distribution.
        
        @param state: A Dict from Node-objects to values. You can specify the 
            values of this nodes parents in this dict and the conditional 
            probability density will be adjusted accordingly.
        '''
        proposal=self.cpd.sample_global(state)
        return proposal
        
    def get_probability(self, value, state):
        '''
        This method can be used to query the cpd for how probable a value is,
        given this nodes markov-blanket.
        
        @param value: The value for this random-variable.
        @param state: A Dict from Node-objects to values. Should at least contain
            all variables from this nodes markov-blanket.
        '''
        return self.cpd.get_probability(value, state)
        
