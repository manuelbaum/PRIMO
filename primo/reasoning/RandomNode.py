# -*- coding: utf-8 -*-

from primo.core import Node
#from primo.reasoning.density import Density


class RandomNode(Node):
    '''Represents a random variable. There should be subclasses of this for
    different kinds of data. There are currently DiscreteNode for discrete-valued
    random variables and ContinuousNode for random Variables with R or an Intervall
    in R as domain.
    
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
        
