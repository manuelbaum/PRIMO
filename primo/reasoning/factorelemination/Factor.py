
from primo.core import Node

class Factor(object):


    cluster = set()
    isEvidence = False
    
    
    def __init__(self,node):
        self.node = node
        self.calCPD = node.get_cpd().copy()
        
    def __str__(self):
        return self.node.name
        
    def set_evidence(self,evd):
        self.calCPD = self.node.get_cpd().copy()
        self.calCPD = self.calCPD.set_evidence(evd)
        self.isEvidene = True
        
    def clear_evidence(self):
        self.calCPD = self.node.get_cpd().copy()
        self.isEvidence = False
        
    def set_cluster(self,cluster):
        self.cluster = cluster
        
    def get_variables(self):
        return self.node.get_cpd().variables
        
    def get_calculation_CDP(self):
        return self.calCPD;
        
    def get_node(self):
        return self.node
        
    def contains_node(self,node):
        return self.node == node
    
    
