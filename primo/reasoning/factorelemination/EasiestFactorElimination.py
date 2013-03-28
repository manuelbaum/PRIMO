#!/usr/bin/env python
# -*- coding: utf-8 -*-
from  primo.core import BayesNet
from  primo.reasoning import DiscreteNode
import numpy

class EasiestFactorElimination(object):
    '''This is the easiest way for factor elimination.It's has the worst runtime because:
    1.* Needed evidences are set.
    2. All nodes are multiplied.
    3. The redundant variables are summed out'''
    
    
    
    def __init__(self,bayesNet):
        self.bn= bayesNet

        
    def calculate_PriorMarginal(self,variables):  
        '''Calculates the prior marignal for the given variables. The resulting
        CPD is returned.'''
        nodes = self.bn.get_all_nodes()
        
        finCpd = nodes.pop().get_cpd()
        
        for n in nodes:
            finCpd = finCpd.multiplication(n.get_cpd())
            
        for v in finCpd.get_variables()[:]:
            if v not in variables:
                finCpd = finCpd.marginalization(v)
        
        return finCpd
        
    def calculate_PosteriorMarginal(self,variables,evidence):
        '''Calculates the posterior marginal for given variables and evidence.
        It returns the resulting cpd.'''
        nodes = self.bn.get_all_nodes()
        
        #List of evidences
        ev_list = zip(*evidence)     
        # Special Case: First Node
        node1 = nodes.pop()
        if node1 in ev_list[0]:
            ind = ev_list[0].index(node1)
            finCpd = node1.get_cpd().set_evidence(evidence[ind])
            
        else:
            finCpd = node1.get_cpd()
            
            
        # For all other nodes
        for n in nodes:
            if n in ev_list[0]:
                #Set evidence and multiply
                ind = ev_list[0].index(n)
                nCPD = n.get_cpd().set_evidence(evidence[ind])
                finCpd = finCpd.multiplication(nCPD)            
            else:
                #only multiply
                finCpd = finCpd.multiplication(n.get_cpd())

                
        for v in finCpd.get_variables()[:]:
            if v not in variables:
                finCpd = finCpd.marginalization(v)
                
        finCpd = finCpd.normalize_as_jpt()
        
            
        return finCpd
        
        
        
    def calculate_PoE(self,evidence):
        ''' Calculates the probabilty of evidence for the given evidence and returns the result.'''
        
        nodes = self.bn.get_all_nodes()
        
        unzipped_list = zip(*evidence)
              
        node1 = nodes.pop()
        if node1 in unzipped_list[0]:
            ind = unzipped_list[0].index(node1)
            finCpd = node1.get_cpd().set_evidence(evidence[ind])
            
        else:
            finCpd = node1.get_cpd()
                  
        for n in nodes:
            if n in unzipped_list[0]:
                ind = unzipped_list[0].index(n)
                nCPD = n.get_cpd().set_evidence(evidence[ind])
                finCpd = finCpd.multiplication(nCPD)
            else:
                finCpd = finCpd.multiplication(n.get_cpd())
          
        for v in finCpd.get_variables()[:]:
            finCpd = finCpd.marginalization(v)
            
        return finCpd
