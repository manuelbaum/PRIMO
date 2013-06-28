import abc
import re



class Node(object):
    __metaclass__ = abc.ABCMeta

    name = "UninitializedName"
    position = (0, 0)

    def __init__(self, node_name):
        # Remove all special characters and replace " " with "_"
        name = re.sub(r"[^a-zA-Z_0-9 ]*", "", node_name)
        self.name = name.replace(" ", "_")        
        # for visual illustration
        self.pos = (0, 0)

 #   @abc.abstractmethod
 #   def announce_parent(self, node):
 #       """This method will be called by the graph-management to inform nodes
 #       which just became children of other nodes, so they can adapt themselves
 #       (e.g. their cpt)"""
 #       return

    def set_cpd(self, cpd):
        self.cpd = cpd
        
    def get_cpd(self):
        return self.cpd

    def announce_parent(self, node):
        self.cpd.add_variable(node)

    def get_cpd_reduced(self, evidence):
        return self.cpd.reduction(evidence)

    def get_value_range(self):
        return self.value_range

    def __str__(self):
        print self.name
        return self.name
