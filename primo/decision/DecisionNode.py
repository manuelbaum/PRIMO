# -*- coding: utf-8 -*-

from primo.core import Node


class DecisionNode(Node):
    """Handles a DecisionNode which contains a list of actions and has a state"""
    
    def __init__(self, name, value_range):
        """
        Initialize a DecisionNode
        
        Keyword arguments:
        
        name -- Name of this DecisionNode
        value_range -- A list of actions
        """
        super(DecisionNode, self).__init__(name)
        self.value_range = value_range
        self.state = None
    
    def get_value_range(self):
        """returns a list of actions"""
        return self.value_range
    
    def set_value_range(self, value_range):
        """
        Sets the value range
        
        Keyword arguments:
        value_range -- List of actions
        """
        self.value_range = value_range
    
    def announce_parent(self, node):
        pass
    
    def set_state(self, decision):
        """
        Sets the state of this Decision Node
        
        Keyword arguments:
        
        decision -- The decision that has been made
        """
        if decision in self.value_range:
            self.state = decision
        else:
            raise Exception("Could not set the state, given decision is not in value range")
        
    def get_state(self):
        """
        Getter for the state
        """
        return self.state
    
    def __str__(self):
        return self.name + "\n" + str(self.value_range) + "\n" + str(self.state)
