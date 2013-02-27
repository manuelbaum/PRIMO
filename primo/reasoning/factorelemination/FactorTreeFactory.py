
import networkx as nx
from primo.core import Node
from primo.reasoning.factorelemination import Factor
from primo.reasoning.factorelemination import FactorTree
from random import choice

class FactorTreeFactory(object):
    
    def create_random_factortree(self,bayesNet):
        allNodes = bayesNet.get_all_nodes()
        
        if len(allNodes) == 0:
            raise Exception("createRandomFactorTree: No nodes in given bayesNet")
        
        tn = allNodes.pop()
        rootFactor = Factor(tn)

        graph = nx.DiGraph()

        graph.add_node(rootFactor)        
        
        usedNodes = [rootFactor]
        
        for n in allNodes[:]:
            parentNode = choice(usedNodes[:])
            newFactor = Factor(n)
            graph.add_edge(parentNode,newFactor)
            usedNodes.append(newFactor)
            
            
        return FactorTree(graph,rootFactor)
            
        
        
    
