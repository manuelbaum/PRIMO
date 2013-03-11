# -*- coding: utf-8 -*-

from primo.core import BayesNet


class TwoTBN(BayesNet):
    ''' This is the implementation of a 2-time-slice Bayesian network (2-TBN).
    '''

    def __init__(self):
        BayesNet.__init__(self)


    def add_edge(self, node_from, node_to, inter=False):
        '''Add an directed edge to the graph.

        Keyword arguments:
        node_from -- from node
        node_to -- to node
        inter -- is this edge a temporal (inter-slice) conditional dependency
        (default: False)
        '''
        super(TwoTBN, self).add_edge(node_from, node_to)
        # Adding an edge that already exists updates the edge data.
        self.graph[node_from][node_to]['inter'] = inter

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
        for successor in self.graph.successors(node):
            if self.graph[node][successor]['inter']:
                return False
            if successor == origin:
                return True
            else:
                return self.has_loop(successor, origin)

    def get_nodes_in_topological_sort(self):
        # Remove temporal/inter-slice edges for toplogical sort
        inter_edges = []
        for edge in self.graph.edges(data = True):
            if edge[2]['inter'] == True:
                inter_edges.append(edge)

        self.graph.remove_edges_from(inter_edges)
        ts = super(TwoTBN, self).get_nodes_in_topological_sort()
        # Add temporal/inter-slice edges
        self.graph.add_edges_from(inter_edges)
        return ts