# -*- coding: utf-8 -*-

from primo.reasoning import RandomNode
import random
import scipy

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
        
    def __repr__(self):
        return "str(ContinuousNode)"+self.name+")"
        
    def set_density_parameters(self, density_parameters):
        self.cpd.set_parameters(density_parameters)
        
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
        std_walk=1.0
        
        #intersect possible evidence-interval with value_range:
        if self in evidence.keys():
            evidence_range=evidence[self].get_interval()
            lower_limit=max(self.value_range[0],evidence_range[0])
            upper_limit=min(self.value_range[1],evidence_range[1])
        else:
            lower_limit=self.value_range[0]
            upper_limit=self.value_range[1]
        
        if lower_limit==upper_limit:
            v=lower_limit
        if lower_limit>upper_limit:
            raise Exception("Intersection of random variable's value_range and"
                "allowed Interval for Evidence is empty - no sampling possible")
        
        #generate the actual sample
        distribution=scipy.stats.norm(x, std_walk)
        lower_cdf=distribution.cdf(lower_limit)
        upper_cdf=distribution.cdf(upper_limit)
        
        sample_in_integral=random.uniform(lower_cdf, upper_cdf)
        
        sample=distribution.ppf(sample_in_integral)
        
        
        
        a=scipy.stats.norm(self.value_range[0], std_walk).cdf(x)
        b=scipy.stats.norm(self.value_range[0], std_walk).cdf(sample)
        cdf_ratio = a/b 
        return sample,cdf_ratio
        
    def sample_global(self, state, evidence):
        '''
        This method can be used to sample from this local distribution.
        
        @param state: A Dict from Node-objects to values. You can specify the 
            values of this nodes parents in this dict and the conditional 
            probability density will be adjusted accordingly.
        '''
        #is there some evidence for this node?
        if self in evidence.keys():
            #if only one value is allowed we can return it immediatly
            unique=evidence[self].get_unique_value()
            if unique!=None:
                return unique
            #if a whole interval is allowed intersect it with this variable's
            #value_range to get limits for sampling
            else:
                evidence_range=evidence[self].get_interval()
                lower_limit=max(self.value_range[0],evidence_range[0])
                upper_limit=min(self.value_range[1],evidence_range[1])
        #without evidence this variable's value_range represents limits for sampling
        else:
            lower_limit=self.value_range[0]
            upper_limit=self.value_range[1]
        #check if only one value is allowed and in case return immediatly
        if lower_limit==upper_limit:
            return lower_limit
        #check for empty interval
        if lower_limit>upper_limit:
            raise Exception("Intersection of random variable's value_range and"
                "allowed Interval for Evidence is empty - no sampling possible")
        
        proposal=self.cpd.sample_global(state,lower_limit,upper_limit)
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
        
