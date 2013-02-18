# -*- coding: utf-8 -*-

from primo.core import Node
from primo.decision.UtilityTable import UtilityTable

class UtilityNode(Node):
    '''Handles an UtilityNode'''
    
    def __init__(self, name):
        super(UtilityNode, self).__init__(name)
        self.ut = UtilityTable()
        
    def announce_parent(self, node):
        self.ut.add_variable(node)
        
    def set_utility_table(self, table, nodes):
        self.ut.set_utility_table(table, nodes)
        
    def set_utility(self, value, assignment):
        self.ut.set_utility(value, assignment)
      
    def get_utility_table(self):
        return self.ut
    
    def get_utility(self, node_value_pairs):
        return self.ut.get_utility(node_value_pairs)
    
    def __str__(self):
        return self.name + "\n" + str(self.ut)    