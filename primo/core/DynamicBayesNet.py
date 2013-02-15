# -*- coding: utf-8 -*-

from primo.core import BayesNet
from primo.core import TwoTBN


class DynamicBayesNet(BayesNet):
    ''' This is the implementation of a dynamic Bayesian network (also called 
    temporal Bayesian network). 
    
    Definition: DBN is a pair (B0, TwoTBN), where B0 is a BN over X(0), 
    representing the initial distribution over states, and TwoTBN is a 
    2-TBN for the process.
    See Koller, Friedman - "Probabilistic Graphical Models" (p. 204)
    
    Properties: Markov property, stationary, directed, discrete, 
    acyclic (within a slice)
    '''

    __B0 = BayesNet() 
    __twoTBN = TwoTBN()
    
    def __init__(self):
        super(DynamicBayesNet, self).__init__()
        
    
    def set_B0(self, B0):
        ''' Set the Bayesian network representing the initial distribution.'''
        if isinstance(B0, BayesNet):
            if not B0.is_valid():
                raise Exception("BayesNet is not valid.")
            self.__B0 = B0
        else:
            raise Exception("Can only set 'BayesNet' and its subclasses as " +
            "B0 of a DBN.")
        
    def set_TwoTBN(self, twoTBN):
        ''' Set the 2-time-slice Bayesian network.'''
        if isinstance(twoTBN, TwoTBN):
            if not twoTBN.is_valid():
                raise Exception("BayesNet is not valid.")
            self.__twoTBN = twoTBN
        else:
            raise Exception("Can only set 'TwoTBN' and its subclasses as " +
            "twoTBN of a DBN.")
            
    def get_B0(self):
        ''' Get the Bayesian network representing the initial distribution.'''
        return self.__B0;
        
    def get_TwoTBN(self):
        ''' Get the 2-time-slice Bayesian network.'''
        return self.__twoTBN;