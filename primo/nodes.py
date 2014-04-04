import abc
import random
import re

import scipy

from primo.reasoning.density import Beta
from primo.reasoning.density import Exponential
from primo.reasoning.density import Gauss
from primo.reasoning.density import ProbabilityTable

class Node(object):

    __metaclass__ = abc.ABCMeta
    name = "UninitializedName"
    position = (0, 0)

    def __init__(self, node_name):
        # Remove all special characters and replace " " with "_"
        name = re.sub(r"[^a-zA-Z_0-9 ]*", "", node_name)
        self.name = name.replace(" ", "_")        
        # for visual illustration
        self.pos = (0, 0)

    def __str__(self):
        return self.name


class RandomNode(Node):
    '''Represents a random variable. There should be subclasses of this for
    different kinds of data. There are currently DiscreteNode for 
    discrete-valued random variables and ContinuousNode for random Variables
    with R or an Intervall in R as domain.
    
    At a later point in time there may be structural nodes too.
    '''

    #The Continditional Propability Distribution of this random variable
    cpd = None

    def __init__(self, name):
        super(RandomNode, self).__init__(name)
        
        #value_range defines the domain of this random variable
        self.value_range=None

    def set_cpd(self, cpd):
        self.cpd = cpd
        
    def get_cpd(self):
        return self.cpd

    def announce_parent(self, node):
        '''
        Adjust the cpd so a new node is incorporated as dependency.
        '''
        self.cpd.add_variable(node)

    def get_cpd_reduced(self, evidence):
        '''
        Return a reduced version of the cpd of this node. This reduced version
        is constructed according to some evidence.
        @param evidence: A List of (Node,Value) pairs.
        '''
        return self.cpd.reduction(evidence)

    def get_value_range(self):
        return self.value_range
        
    def sample_gobal(self, x, evidence=None):
        '''
        This method can be used to sample from this local distribution.
        
        @param state: A Dict from Node-objects to values. You can specify the 
            values of this nodes parents in this dict and the conditional 
            probability density will be adjusted accordingly.
        '''
        raise Exception("Called unimplemented Method")
        
    def sample_local(self, x, evidence=None):
        '''
        This method can be used to do a random walk in the domain of this node.
        
        @param x: The spot around which the next sample shall be generated.
        @param evidence: Evidence which is to be concerned when new samples are
            being generated. I am not entirely sure that this belongs here or is
            correct in theory...
        '''
        raise Exception("Called unimplemented Method")


    def is_valid(self):
        raise Exception("Called an unimplemented function")


class DiscreteNode(RandomNode):
    '''#TODO: write doc'''

    def __init__(self, name, value_range):
        super(DiscreteNode, self).__init__(name)

        self.value_range = value_range
        self.cpd = ProbabilityTable()
        self.cpd.add_variable(self)
        
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return "DiscreteNode("+self.name+")"

    def set_probability(self, value, node_value_pairs):
        self.cpd.set_probability(value, node_value_pairs)
        
    def get_probability(self, value, node_value_pairs):
        return self.cpd.get_probability([(self,value)] + node_value_pairs)

    def set_probability_table(self, table, nodes):
        self.cpd.set_probability_table(table, nodes)

    def is_valid(self):
        return self.cpd.is_normalized_as_cpt(self)
        
    def sample_global(self, state, evidence):
        if evidence==None or not self in evidence.keys():
            compatibles=self.value_range
        else:
            compatibles=[]
            for v in self.value_range:
                if evidence[self].is_compatible(v):
                    compatibles.append(v)
        
        return self.cpd.sample_global(state,self,compatibles)
        
    def sample_local(self, x, evidence=None):
        if evidence==None or not self in evidence.keys():
            compatibles=self.value_range
        else:
            compatibles=[]
            for v in self.value_range:
                if evidence[self].is_compatible(v):
                    compatibles.append(v)
        
        return random.choice(compatibles), 1.0


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


class ContinuousNodeFactory(object):
    '''This class offers methods for generating ContinuousNodes'''
    def __init__(self):
        pass
        
    def createGaussNode(self, name):
        '''
        Create a LinearGaussNode with linear dependencies on parents.
        
        @param name: The name of the node.
        '''        
        return self.createContinuousNode(name,(-float("Inf"),float("Inf")),Gauss)
        
    def createExponentialNode(self, name):
        '''
        Create a LinearExponentialNode with linear dependencies on parents.
        
        @param name: The name of the node.
        '''  
        return self.createContinuousNode(name,(0,float("Inf")),Exponential)
        
    def createBetaNode(self, name):
        '''
        Create a LinearBetaNode with linear dependencies on parents.
        
        @param name: The name of the node.
        '''  
        return self.createContinuousNode(name,(0,1),Beta)
    
    def createContinuousNode(self,name,value_range,DensityClass):
        '''
        Create a ContinuousNode. This method should only be invoked from
        outside this class if no specialized method is available.
        
        @param name: The name of the node.
        @param value_range: A 2-tuple which represents the interval that is the
            domain of the variable.
        @param DensityClass: A class from primo.reasoning.density that shall be
            the node's pdf
        '''  
        return ContinuousNode(name,value_range,DensityClass)

