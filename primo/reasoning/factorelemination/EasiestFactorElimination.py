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
        #TODO
        # Verbundwahrscheinlichkeit / PoE
        # Erst wie Prior Marginal nur mit setzen der Evidence
        # Dann PoE berechnen und damit normalisieren
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
        
        
        
    def calculate_PoE(self,evidence):
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
