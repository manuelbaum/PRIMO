import abc

class Node(object):
    __metaclass__ = abc.ABCMeta

    name = "UninitializedName"

    def __init__(self, node_name):
        self.name = node_name

    @abc.abstractmethod
    def announce_parent(self, node):
        """This method will be called by the graph-management to inform nodes which just
            became children of other nodes, so they can adapt themselves (e.g. their cpt)"""
        return

    def __str__(self):
        print self.name
        return self.name
