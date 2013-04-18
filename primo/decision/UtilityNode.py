# -*- coding: utf-8 -*-

from primo.core import Node
from primo.decision.UtilityTable import UtilityTable

class UtilityNode(Node):
    """Handles an UtilityNode"""
    
    def __init__(self, name):
        """
        Construktor for the Utility Node
        
        Keyword arguments:
        
        name -- The name of this node
        """
        super(UtilityNode, self).__init__(name)
        self.ut = UtilityTable()
        
    def announce_parent(self, node):
        """
        Gets called automatically when this node gets a new parent
        
        Keyword arguments:
        
        node -- the parent node of this utility node
        """
        self.ut.add_variable(node)
        
    def set_utility_table(self, table, nodes):
        """
        Sets the utility table
        
        keyword arguments:
        table -- the utility table
        nodes -- a list of nodes which are the parents of this utility node
        """
        self.ut.set_utility_table(table, nodes)
        
    def set_utility(self, value, assignment):
        """
        Sets one utility in the utility table of this node
        
        keyword arguments:
        value -- the utlity value
        assignment -- a list of assignments of node value pairs
        """
        self.ut.set_utility(value, assignment)
      
    def get_utility_table(self):
        """
        Getter for the utility table
        """
        return self.ut
    
    def get_utility(self, node_value_pairs):
        """
        Getter for the utility stored in the utility table
        
        keyword arguments:
        node_value_pairs -- list of node,value pairs
        """
        return self.ut.get_utility(node_value_pairs)
    
    def __str__(self):
        return self.name + "\n" + str(self.ut)    