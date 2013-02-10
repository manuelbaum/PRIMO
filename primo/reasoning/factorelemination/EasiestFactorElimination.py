#!/usr/bin/env python
# -*- coding: utf-8 -*-
from  primo.core import BayesNet
from  primo.reasoning import DiscreteNode
import numpy

class EasiestFactorElimination(object):
    '''This is the easiest way for factor elimination. But not
    very efficient.'''
    
    
    
    def __init__(self):
        self.bn= BayesNet()

    def set_BayesNet(self,bayesnet):
        self.bn = bayesnet
        
    def calculate_PriorMarginal(self,variables):        
        nodes = self.bn.get_all_nodes()
        
        finCpd = nodes.pop().get_cpd()
        
        for n in nodes:
            finCpd = finCpd.multiplication(n.get_cpd())
            
        for v in finCpd.get_variables()[:]:
            if v not in variables:
                finCpd = finCpd.marginalization(v)
        
        return finCpd
        
    def calculate_PosteriorMarginal(self,variables,evidence):
        bn = bn.copy()
        
        
    def calculate_PoE(self,evidence):
        bn = bn.copy()
        
        
