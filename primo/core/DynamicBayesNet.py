# -*- coding: utf-8 -*-

from primo.core import BayesNet


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
        super(DynamicBayesNet, self).add_edge(node_from, node_to)
        # Adding an edge that already exists updates the edge data.
        self.graph[node_from][node_to]['arc'] = arc

    def is_valid(self):
        '''Check if graph structure is valid.
        Returns true if graph is directed and acyclic, false otherwiese'''

        for node in self.graph.nodes():
            if self.has_loop(node):
                return False

        return True

    def has_loop(self, node, origin=None):
        '''Check if any path from node leads back to node (except temporal
        conditional dependencies).

        Keyword arguments:
        node -- the start node
        origin -- for internal recursive loop (default: None)

        Returns true on succes, false otherwise.'''
        if not origin:
            origin = node
        print("has_loop DBN")
        for successor in self.graph.successors(node):
            if self.graph[node][successor]['arc']:
                print("### Found arc.")
                return False
            if successor == origin:
                self.graph.n
                return True
            else:
                return self.has_loop(successor, origin)

