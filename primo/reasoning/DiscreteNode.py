# -*- coding: utf-8 -*-

from primo.reasoning import RandomNode
from primo.reasoning.density import ProbabilityTable
import random


class DiscreteNode(RandomNode):
    '''#TODO: write doc'''

    def __init__(self, name, value_range):
        super(DiscreteNode, self).__init__(name)

        self.value_range = value_range
        self.cpd = ProbabilityTable()
        self.cpd.add_variable(self)
        
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return "DiscreteNode("+self.name+")"

    def set_probability(self, value, node_value_pairs):
        self.cpd.set_probability(value, node_value_pairs)
        
    def get_probability(self, value, node_value_pairs):
        return self.cpd.get_probability([(self,value)] + node_value_pairs)

    def set_probability_table(self, table, nodes):
        self.cpd.set_probability_table(table, nodes)

    def is_valid(self):
        return self.cpd.is_normalized_as_cpt(self)
        
    def sample_global(self, evidence=None):
        if evidence==None or not self in evidence.keys():
            compatibles=self.value_range
        else:
            compatibles=[]
            for v in self.value_range:
                if evidence[self].is_compatible(v):
                    compatibles.append(v)
        
        return random.choice(compatibles)
        
    def sample_local(self, x, evidence=None):
        if evidence==None or not self in evidence.keys():
            compatibles=self.value_range
        else:
            compatibles=[]
            for v in self.value_range:
                if evidence[self].is_compatible(v):
                    compatibles.append(v)
        
        return random.choice(compatibles)
