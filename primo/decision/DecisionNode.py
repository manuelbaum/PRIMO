# -*- coding: utf-8 -*-

from primo.core import Node


class DecisionNode(Node):
    '''Handles a DecisionNode which contains a list of actions'''
    
    def __init__(self, name, value_range):
        '''Initialize a DecisionNode
        Keyword arguments:
        
        name -- Name of this DecisionNode
        value_range -- A list of actions
        '''
        super(DecisionNode, self).__init__(name)
        self.value_range = value_range
        self.state = None
    
    def get_value_range(self):
        '''returns a set of actions'''
        return self.value_range
    
    def set_value_range(self, value_range):
        self.value_range = value_range
    
    def announce_parent(self, node):
        pass
    
    def set_state(self, decision):
        self.state = decision
        
    def get_state(self):
        return self.state
    
    def __str__(self):
        return self.name + "\n" + str(self.value_range) + "\n" + str(self.state)
