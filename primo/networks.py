import networkx as nx

import primo.nodes

class BayesianNetwork(object):

    def __init__(self):
        self.graph = nx.DiGraph()
        self.node_lookup = {}

    def add_node(self, node):
        if isinstance(node, primo.nodes.Node):
            if node.name in self.node_lookup.keys():
                raise Exception("Node name already exists in Bayesnet: "+node.name)
            self.node_lookup[node.name]=node
            self.graph.add_node(node)
        else:
            raise Exception("Can only add 'Node' and its subclasses as nodes into the BayesianNetwork")

    def add_edge(self, node_from, node_to):
        if node_from in self.graph.nodes() and node_to in self.graph.nodes():
            self.graph.add_edge(node_from, node_to)
            node_to.announce_parent(node_from)
        else:
            raise Exception("Tried to add an Edge between two Nodes of which at least one was not contained in the Bayesnet")

    def remove_node(self, node):
        if node.name not in self.node_lookup.keys():
            raise Exception("Node " + node.name + "does not exists")
        else :
            try:
                self.graph.remove_node(node)
            except nx.exception.NetworkXError:
                raise Exception("Tried to remove a node which does not exist.")
            del self.node_lookup[node.name]

    def remove_edge(self, node_from, node_to):
        try:
            self.graph.remove_edge(node_from, node_to)
        except nx.exception.NetworkXError:
            raise Exception("Tried to remove an edge which does not exist in the BayesianNetwork")
        #raise Exception("Fixme: Adapt CPD of child-node")

    def get_node(self, node_name):
        try:
            return self.node_lookup[node_name]
        except KeyError:
            raise Exception("There is no node with name "+node_name+" in the BayesianNetwork")

    def get_all_nodes(self):
        return self.graph.nodes()

    def get_nodes(self, node_names=[]):
        nodes = []
        if not node_names:
            nodes = self.graph.nodes()
        else:
            for node_name in node_names:
                nodes.append(self.get_node(node_name))
        return nodes

    def get_nodes_in_topological_sort(self):
        return nx.topological_sort(self.graph)

    def get_parents(self, node):
        if node.name not in self.node_lookup.keys():
            raise Exception("Node " + node.name + "does not exists")
        else:
            return self.graph.predecessors(node)


    def get_children(self, node):
        if node.name not in self.node_lookup.keys():
            raise Exception("Node " + node.name + "does not exists")
        else:
            return self.graph.successors(node)


    def get_markov_blanket(self, node):
        raise Exception("Called unimplemented function")

    def is_dag(self):
        raise Exception("Called unimplemented function")

    def draw(self):
        import matplotlib.pyplot as plt
        nx.draw_circular(self.graph)
        plt.show()

    def draw_graphviz(self):
        import matplotlib.pyplot as plt
        nx.draw_graphviz(self.graph)
        plt.show()

    def is_valid(self):
        '''Check if graph structure is valid.
        Returns true if graph is directed and acyclic, false otherwiese'''

        if self.graph.number_of_selfloops() > 0:
            return False

        for node in self.graph.nodes():
            if self.has_loop(node):
                return False

        return True

    def has_loop(self, node, origin=None):
        '''Check if any path from node leads back to node.

        Keyword arguments:
        node -- the start node
        origin -- for internal recursive loop (default: None)

        Returns true on succes, false otherwise.'''
        if not origin:
            origin = node

        for successor in self.graph.successors(node):
            if successor == origin:
                return True
            else:
                return self.has_loop(successor, origin)

    def clear(self):
        '''Remove all nodes and edges from the graph.
        This also removes the name, and all graph, node and edge attributes.'''
        self.graph.clear()
        self.node_lookup.clear()

    def number_of_nodes(self):
        '''Return the number of nodes in the graph.'''
        return len(self)

    def __len__(self):
        '''Return the number of nodes in the graph.'''
        return len(self.graph)


class BayesianDecisionNetwork(BayesianNetwork):

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
            raise Exception("Can only add 'Node' and its subclasses as nodes into the BayesianNetwork")

    def get_all_nodes(self):
        '''Returns all RandomNodes'''
        return self.random_nodes

    def get_all_decision_nodes(self):
        return self.decision_nodes

    def get_all_utility_nodes(self):
        return self.utility_nodes

    def add_edge(self, node_from, node_to):
        """
        Adds an edge between two nodes. It is impossible to create en edge between two decision nodes and between two
        utility nodes.

        keyword arguments:
        node_from -- Node from where the edge shall begin
        node_to -- Node where the edge shall end
        """
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
        """
        Resets all decisions in the Bayesian Decision Network
        """
        for node in self.decision_nodes:
            node.set_state(None)

    def get_partialOrdering(self):
        """
        Getter for the partial ordere
        """
        return self.partialOrdering

    def set_partialOrdering(self, partialOrder):
        """
        Sets the partial ordering for this Bayesian Decision Network

        partialOrder -- ordered list of RandomNodes and Decision Nodes
        example: [decisionNode1, [randomNode1,randomNode2], decisionNode2, [randomNode3]]
        """
        self.partialOrdering = partialOrder


class DynamicBayesianNetwork(BayesianNetwork):
    ''' This is the implementation of a dynamic Bayesian network (also called
    temporal Bayesian network).

    Definition: DBN is a pair (B0, TwoTBN), where B0 is a BN over X(0),
    representing the initial distribution over states, and TwoTBN is a
    2-TBN for the process.
    See Koller, Friedman - "Probabilistic Graphical Models" (p. 204)

    Properties: Markov property, stationary, directed, discrete,
    acyclic (within a slice)
    '''

    def __init__(self):
        super(DynamicBayesianNetwork, self).__init__()
        self._B0 = BayesianNetwork()
        self._twoTBN = TwoTBN()

    @property
    def B0(self):
        ''' Get the Bayesian network representing the initial distribution.'''
        return self._B0

    @B0.setter
    def B0(self, value):
        ''' Set the Bayesian network representing the initial distribution.'''
        if isinstance(value, BayesianNetwork):
            if not value.is_valid():
                raise Exception("BayesianNetwork is not valid.")
            self._B0 = value
        else:
            raise Exception("Can only set 'BayesianNetwork' and its subclasses as " +
            "B0 of a DBN.")

    @property
    def twoTBN(self):
        ''' Get the 2-time-slice Bayesian network.'''
        return self._twoTBN

    @twoTBN.setter
    def twoTBN(self, value):
        ''' Set the 2-time-slice Bayesian network.'''
        if isinstance(value, TwoTBN):
            if not value.is_valid():
                raise Exception("BayesianNetwork is not valid.")
            self._twoTBN = value
        else:
            raise Exception("Can only set 'TwoTBN' and its subclasses as " +
            "twoTBN of a DBN.")

    def is_valid(self):
        '''Check if graph structure is valid. And if there is a same-named
        inital node in towTBN for every node in BO.
        Returns true if graph is directed and acyclic, false otherwiese'''
        for node in self._B0.get_nodes():
            if not self._twoTBN.has_initial_node_by_name(node.name):
                print("Node with name " + str(node.name) +
                " not found in TwoTBN!")
                return False;

        return super(DynamicBayesianNetwork, self).is_valid()


class TwoTBN(BayesianNetwork):
    ''' This is the implementation of a 2-time-slice Bayesian network (2-TBN).
    '''

    def __init__(self, bayesnet=None):
        BayesianNetwork.__init__(self)
        if bayesnet:
            if not isinstance(bayesnet, BayesianNetwork):
                raise Exception("Parameter 'bayesnet' is not a instance of class BayesianNetwork.")
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
