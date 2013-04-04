# -*- coding: utf-8 -*-

from primo.core import BayesNet
from primo.core import TwoTBN


class DynamicBayesNet(BayesNet):
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
        super(DynamicBayesNet, self).__init__()
        self._B0 = BayesNet()
        self._twoTBN = TwoTBN()

    @property
    def B0(self):
        ''' Get the Bayesian network representing the initial distribution.'''
        return self._B0

    @B0.setter
    def B0(self, value):
        ''' Set the Bayesian network representing the initial distribution.'''
        if isinstance(value, BayesNet):
            if not value.is_valid():
                raise Exception("BayesNet is not valid.")
            self._B0 = value
        else:
            raise Exception("Can only set 'BayesNet' and its subclasses as " +
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
                raise Exception("BayesNet is not valid.")
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

        return super(DynamicBayesNet, self).is_valid()