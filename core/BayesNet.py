import sys

sys.path.append("lib/networkx-1.7-py2.7.egg")
import networkx as nx
from core.Node import Node

class BayesNet(object):
    graph = nx.DiGraph()
    node_lookup = {}

    def __init__(self):
        pass

    
    def add_node(self, node):
        if isinstance(node, Node):
            if node.name in self.node_lookup.keys():
                raise Exception("Node name already exists in Bayesnet: "+node.name)
            self.node_lookup[node.name]=node
            self.graph.add_node(node)
        else:
            raise Exception("Can only add 'Node' and its subclasses as nodes into the BayesNet")

    def add_edge(self, node_from, node_to):
        if node_from in self.graph.nodes() and node_to in self.graph.nodes():
            self.graph.add_edge(node_from, node_to)

            #raise Exception("Fixme: Adapt CPD of child-node")

        else:
            raise Exception("Tried to add an Edge between two Nodes of which at least one was not contained in the Bayesnet")

    def remove_node(self, node):
        raise Exception("Called unimplemented function")

    def remove_edge(self, node_from, node_to):
        try:
            self.graph.remove_edge(node_from, node_to)
        except nx.exception.NetworkXError:
            raise Exception("Tried to remove an Edge which does not exist in the BayesNet")
        #raise Exception("Fixme: Adapt CPD of child-node")

    def get_node(self, node_name):
        try:
            return self.node_lookup[node_name]
        except KeyError:
            raise Exception("There is no node with name "+node_name+" in the bayesnet")        

    def get_nodes(self, node_names):
        for node_name in node_names:
            yield self.get_node(node_name)

    def get_parents(self, node):
        raise Exception("Called unimplemented function")

    def get_children(self, node):
        raise Exception("Called unimplemented function")

    def get_markov_blanket(self, node):
        raise Exception("Called unimplemented function")

    def is_dag(self):
        raise Exception("Called unimplemented function")

    def draw(self):
        import matplotlib.pyplot as plt
        nx.draw(self.graph)
        plt.show() 
 
