# -*- coding: utf-8 -*-

from primo.core import BayesNet
from primo.reasoning.density import ProbabilityTable


class TwoTBN(BayesNet):
    ''' This is the implementation of a 2-time-slice Bayesian network (2-TBN).
    '''

    def __init__(self, bayesnet=None):
        BayesNet.__init__(self)
        if bayesnet:
            if not isinstance(bayesnet, BayesNet):
                raise Exception("Parameter 'bayesnet' is not a instance of class BayesNet.")
            self.graph = bayesnet.graph
            self.node_lookup = bayesnet.node_lookup
        self.__initial_nodes = []

    def create_timeslice(self, state, initial=False):
        '''
        Set all initial nodes to the value of their corresponding nodes
        in state (previous time slice).
        
        Keyword arguments:
        state -- Current state of the network (previous time slice).
        initial -- Set initial to true if this will be the first time slice
        and state only contains nodes of the initial distribution.
        
        Returns this instance with all initial nodes set to their
        new value.
        '''
        for (node, node_t) in self.__initial_nodes:
            cpd = ProbabilityTable()
            cpd.add_variable(node)
            node.set_cpd(cpd)
            if not initial:
                node.set_probability(1., [(node, state[node_t])])
            else:
                for node0 in state:
                    if node0.name == node.name:
                        node.set_probability(1., [(node, state[node0])])
                        continue
        return self


    def add_node(self, node, initial=False, node_t=None):
        '''
        Add a node to the TwoTBN.
        
        Keyword arguments:
        node -- Node to be added.
        initial -- If true node is marked as initial node.
        node_t -- If initial is true this is the corresponding node in the time slice.
        '''
        super(TwoTBN, self).add_node(node)
        if initial:
            self.set_initial_node(node, node_t)
            
    def set_initial_node(self, node_name, node_name_t):
        '''
        Mark a node as initial node.
        
        Keyword arguments:
        node_name -- Name of the initial node.
        node_name_t -- Name of the corresponding node in the time slice.
        '''
        node0 = self.get_node(node_name)
        node1 = self.get_node(node_name_t)
        self.__initial_nodes.append((node0, node1))

    def has_initial_node_by_name(self, node_name):
        '''
        Check if this instance has an inital node with name node_name.
        
        Returns true on success, false otherwise.
        '''
        for (node, node_t) in self.__initial_nodes:
            if node.name == node_name:
                return True
        return False