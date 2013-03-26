# -*- coding: utf-8 -*-

from primo.reasoning import RandomNode
from primo.reasoning.density import ProbabilityTable


class DiscreteNode(RandomNode):
    '''#TODO: write doc'''

    def __init__(self, name, value_range):
        super(DiscreteNode, self).__init__(name)

        self.value_range = value_range
        self.cpd = ProbabilityTable()
        self.cpd.add_variable(self)

    def announce_parent(self, node):
        self.cpd.add_variable(node)

    def __str__(self):
        return self.name # + "\n" + str(self.cpd)

    def set_probability(self, value, node_value_pairs):
        self.cpd.set_probability(value, node_value_pairs)

    def set_probability_table(self, table, nodes):
        self.cpd.set_probability_table(table, nodes)
        
    def get_cpd_reduced(self, evidence):
        return self.cpd.reduction(evidence)

    def get_value_range(self):
        return self.value_range
        
    def set_cpd(self, cpd):
        self.cpd = cpd
        
    def get_cpd(self):
        return self.cpd

    def is_valid(self):
        return self.cpd.is_normalized_as_cpt(self)
