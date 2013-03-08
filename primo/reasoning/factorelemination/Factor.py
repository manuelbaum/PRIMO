
from primo.core import Node

class Factor(object):

    evidence = ""
    cluster = set()
    
    
    def __init__(self,node):
        self.node = node
        self.calCPD = node.get_cpd()
        
    def __str__(self):
        return self.node.name
        
    def set_evidence(self,evd):
        self.evidence = evd
        
    def clear_evidence(self):
        self.evidence = ""
        
    def set_cluster(self,cluster):
        self.cluster = cluster
        
    def get_variables(self):
        return self.node.get_cpd().variables
        
    def get_calculation_CDP(self):
        return self.calCPD;
    
    
