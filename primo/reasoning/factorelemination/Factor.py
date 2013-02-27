
from primo.core import Node

class Factor(object):

    evidence = ""
    
    
    def __init__(self,node):
        self.node = node
        self.calPT = node.get_cpd()
        
    def __str__(self):
        return self.node.name
        
    
    
