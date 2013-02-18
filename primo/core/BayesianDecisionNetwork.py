# -*- coding: utf-8 -*-

import networkx as nx

from primo.core import BayesNet
from primo.core import Node
from primo.decision import DecisionNode
from primo.decision import UtilityNode
from primo.reasoning import DiscreteNode

class BayesianDecisionNetwork(BayesNet):
    
    def __init__(self): 
        super(BayesianDecisionNetwork, self).__init__()
        self.partialOrdering = []
        self.random_nodes = []
        self.decision_nodes = []
        self.utility_nodes = []
        
    def is_valid(self):
        '''Check if graph structure is valid.
        Returns true if graph is directed, acyclic and if there is a path that connects every decision node(consistency check), 
        false otherwise'''

        if self.graph.number_of_selfloops() > 0:
            return False

        for node in self.graph.nodes():
            if self.has_loop(node):
                return False
        
        decisionNodeList = []
        for node in self.get_all_nodes():
            if isinstance(node, DecisionNode):
                decisionNodeList.append(node)
        
        return all([nx.has_path(self.graph, x, y) == True for x in decisionNodeList for y in decisionNodeList])
    
    def add_node(self, node):
        if isinstance(node, Node):
            if node.name in self.node_lookup.keys():
                raise Exception("Node name already exists in Bayesnet: "+node.name)
            if isinstance(node, DiscreteNode):
                self.random_nodes.append(node)
            elif isinstance(node, UtilityNode):
                self.utility_nodes.append(node)
            elif isinstance(node, DecisionNode):
                self.decision_nodes.append(node)
            else:
                raise Exception("Tried to add a node which the Bayesian Decision Network can not work with")
            self.node_lookup[node.name]=node
            self.graph.add_node(node)
        else:
            raise Exception("Can only add 'Node' and its subclasses as nodes into the BayesNet")

    def get_all_nodes(self):
        '''Returns all RandomNodes'''
        return self.random_nodes        
    
    def get_all_decision_nodes(self):
        return self.decision_nodes
        
    def get_all_utility_nodes(self):
        return self.utility_nodes
    
    def add_edge(self, node_from, node_to):
        if isinstance(node_from, DecisionNode) and isinstance(node_to, DecisionNode):
            raise Exception("Tried to add an edge from a DecisionNode to a DecisionNode")
        if isinstance(node_from, UtilityNode) and isinstance(node_to, UtilityNode):
            raise Exception("Tried to add an edge from a UtilityNode to a UtilityNode")
        if node_from in self.graph.nodes() and node_to in self.graph.nodes():
            self.graph.add_edge(node_from, node_to)
            node_to.announce_parent(node_from)
        else:
            raise Exception("Tried to add an Edge between two Nodes of which at least one was not contained in the Bayesnet")
    
    def reset_Decisions(self):
        for node in self.decision_nodes:
            node.set_state(None)
    
    def get_partialOrdering(self):
        return self.partialOrdering
    
    def set_partialOrdering(self, partialOrder):
        ''' Sets the partial ordering for this Bayesian Decision Network
        
        partialOrder -- ordered list of RandomNodes and Decision Nodes
        example: [decisionNode1, [randomNode1,randomNode2], decisionNode2, [randomNode3]]
        '''
        self.partialOrdering = partialOrder