
import networkx as nx
import copy
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

        graph = nx.DiGraph(messagesValid=False)

        graph.add_node(rootFactor)        
        
        usedNodes = [rootFactor]
        
        for n in allNodes[:]:
            parentNode = choice(usedNodes[:])
            newFactor = Factor(n)
            graph.add_edge(parentNode,newFactor, inVars=set(),outVars=set())
            usedNodes.append(newFactor)
            
        self.calculate_seperators_pull(rootFactor,graph)
        self.calculate_seperators_push(rootFactor,graph,set())
        self.intersect_seperators(graph)
        
        self.calculate_clusters(rootFactor,graph,set())
            
            
        return FactorTree(graph,rootFactor)
        
    def calculate_seperators_pull(self,factor,graph):
        
        s = set()  
        pullSet = set()
        
        #find all variables in outgoing edges for factor
        for child in graph.neighbors(factor):
            s = self.calculate_seperators_pull(child,graph)
            # add s to incoming vars from child
            tmp = graph[factor][child]['inVars']
            graph[factor][child]['inVars'] = tmp | s
                    
            pullSet =  s | pullSet
            
        pullSet =  s | set(factor.get_variables())    
        return pullSet
        
    def calculate_seperators_push(self,factor,graph,setOut):

        #add local vars to set
        setOut = set(factor.get_variables()) | setOut
        

        for child in graph.neighbors(factor):
            tmpSet = copy.copy(setOut)
            for child2 in graph.neighbors(factor):
                if (child != child2):
                    tmpSet = tmpSet | graph[factor][child2]['inVars']
            
            #add setOut to outgoing vars from child
            tmp = graph[factor][child]['outVars']
            graph[factor][child]['outVars'] = tmp | tmpSet
                
           
            self.calculate_seperators_push(child,graph,tmpSet)
            

    def intersect_seperators(self,graph):
        
        for n,nbrs in graph.adjacency_iter():
            for nbr,eattr in nbrs.items():
                eattr['seperator'] = eattr['inVars'] & eattr['outVars']
                
    def calculate_clusters(self,factor,graph,parent_seperator):
        
        localCluster = parent_seperator | set(factor.get_variables())
        
        for n in graph.neighbors(factor):
            tmpSeperator = graph[factor][n]['seperator']
            localCluster = localCluster | tmpSeperator
            self.calculate_clusters(n,graph,tmpSeperator)
            
        factor.set_cluster(localCluster)

            
            
                        
        
        
            
        
        
    
