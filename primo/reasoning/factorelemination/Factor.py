
from primo.core import Node

class Factor(object):

    evidence = ""
    cluster = set()
    
    
    def __init__(self,node):
        self.node = node
        self.calPT = node.get_cpd()
        
    def __str__(self):
        return self.node.name
        
    def set_evidence(self,evd):
        self.evidence = evd
        
    def clear_evidence(self):
        self.evidence = ""
        
    def set_cluster(self,cluster):
        self.cluster = cluster
        
    def add_to_cluster(self,node):
        self.cluster.add(node)
        
    def get_variables(self):
        return self.node.get_cpd().variables
    
    
