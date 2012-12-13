# -*- coding: utf-8 -*-

from BayesNet import BayesNet


class DynamicBayesNet(BayesNet):

    def __init__(self):
        super(DynamicBayesNet, self).__init__()

    def add_edge(self, node_from, node_to, arc=False):
        '''Add an directed edge to the graph.

        Keyword arguments:
        node_from -- from node
        node_to -- to node
        arc -- is this edge a temporal conditional dependency (default: False)
        '''
        super().add_edge(node_from, node_to)
        # Adding an edge that already exists updates the edge data.
        self.graph.add_edge(node_from, node_to, arc=arc)

