# -*- coding: utf-8 -*-

from primo.core import BayesNet
from primo.reasoning.density import ProbabilityTable


class TwoTBN(BayesNet):
    ''' This is the implementation of a 2-time-slice Bayesian network (2-TBN).
    '''
    __initial_nodes = []

    def __init__(self):
        BayesNet.__init__(self)

    def create_timeslice(self, state):
        for node_x in self.__initial_nodes:
            for node_y in state:
                if node_x.name == node_y.name:
                    cpd = ProbabilityTable()
                    cpd.add_variable(node_x)
                    node_x.set_cpd(cpd)
                    node_x.set_probability(1., [(node_x, state[node_y])])
        return self


    def add_node(self, node, initial=False):
        super(TwoTBN, self).add_node(node)
        if initial:
            self.__initial_nodes.append(node)

    def has_initial_node_by_name(self, node_name):
        '''
        Check if this instance has an inital node with name node_name.
        '''
        for node in self.__initial_nodes:
            if node.name == node_name:
                return True
        return False