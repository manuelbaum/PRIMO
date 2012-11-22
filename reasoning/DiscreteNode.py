# -*- coding: utf-8 -*-

from reasoning.RandomNode import RandomNode
from reasoning.CPD.CPT import CPT

class DiscreteNode(RandomNode):
    '''TODO: write doc'''

    def __init__(self, name, value_range):
        super(DiscreteNode, self).__init__(name)

        self.value_range = value_range
        self.cpd = CPT(self)

    def announce_parent(self, node):
        self.cpd.add_parent(node)

    def __str__(self):
        return self.name + "\n" + str(self.cpd)

    def set_probability(self, value, node_value_pairs):
        self.cpd.set_probability(value, node_value_pairs)
