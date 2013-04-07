
import networkx as nx
import copy
from primo.reasoning.factorelemination import Factor
from primo.reasoning.factorelemination import FactorTree
from random import choice
from operator import itemgetter

class FactorTreeFactory(object):
    '''The FactorTreeFactory creates the FactorTree out of a BayesNet.'''
    
    def create_random_factortree(self,bayesNet):
        ''' Creates a randomly structured FactorTree. This method is useful for testing
        if reasoning works for arbitrary trees.'''
        allNodes = bayesNet.get_all_nodes()
        
        if len(allNodes) == 0:
            raise Exception("createRandomFactorTree: No nodes in given BayesNet")
        
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
        
    def create_greedy_factortree(self,bayesNet):
        '''This method creates a factor the after the following algorithm:
            
            1. Sort factors after containing variables (descending).
            2. For each node in the sorted list insert at it's best position.
            
            The best position is the node with the most joint variables.''' 
        
        allNodes = bayesNet.get_all_nodes()
        
        if len(allNodes) == 0:
            raise Exception("createRandomFactorTree: No nodes in given BayesNet")
            
        sortNodeList = []
        
        for n in allNodes:
            sortNodeList.append((len(n.get_cpd().get_variables()),n))
          
        #sort node list
        sortNodeList = sorted(sortNodeList,key=itemgetter(0),reverse=True)
        
        sortNodeList =  zip(*sortNodeList)
        sortNodeList = list(sortNodeList[1])
        
        #root node with the most variables
        rootFactor = Factor(sortNodeList.pop(0))
        
        #create new graph for factor tree
        graph = nx.DiGraph(messagesValid=False)
        graph.add_node(rootFactor) 
        
        #All nodes are added
        for nd in sortNodeList[:]:
            (ct,insFactor) = self.find_best_node_for_insertion(graph,rootFactor,set(nd.get_cpd().get_variables()))
            nFactor = Factor(nd)
            graph.add_edge(insFactor,nFactor, inVars=set(),outVars=set())
            
        #For the later calculation the seperators are needed
        self.calculate_seperators_pull(rootFactor,graph)
        self.calculate_seperators_push(rootFactor,graph,set())
        self.intersect_seperators(graph)
        
        #the cluster are not necessarily needed but indicate how good the calculation of messages performs
        self.calculate_clusters(rootFactor,graph,set())
            
            
        return FactorTree(graph,rootFactor)
        
        
    def find_best_node_for_insertion(self,graph,factor,nodeSet):
        '''finds the node in the graph with the most common variables to the given node'''
        
        curJointCount = len(set(factor.get_variables()) & nodeSet)
        curInsertFactor = factor
        
        for nbs in graph.neighbors(factor):
            (count,retFactor) = self.find_best_node_for_insertion(graph,nbs,nodeSet)
            if count >= curJointCount:
                curJointCount = count
                curInsertFactor = retFactor
                
        return (curJointCount,curInsertFactor)
            
        
    def calculate_seperators_pull(self,factor,graph):
        
        s = set()  
        pullSet = set(factor.get_variables())
        
        #find all variables in outgoing edges for factor
        for child in graph.neighbors(factor):
            s = self.calculate_seperators_pull(child,graph)
            graph[factor][child]['inVars'] =  s
                    
            pullSet =  s | pullSet
               
        return pullSet
        
    def calculate_seperators_push(self,factor,graph,setOut):

        #add local vars to set
        setOut = set(factor.get_variables()) | setOut
        

        for child in graph.neighbors(factor):
            tmpSet = copy.copy(setOut)
            for child2 in graph.neighbors(factor):
                if (child != child2):
                    tmpSet = tmpSet | graph[factor][child2]['inVars']
            
            #add setOut to outgoing variables from the child
            tmp = graph[factor][child]['outVars']
            graph[factor][child]['outVars'] = tmp | tmpSet
                
           
            self.calculate_seperators_push(child,graph,tmpSet)
            

    def intersect_seperators(self,graph):
        
        for n,nbrs in graph.adjacency_iter():
            for nbr,eattr in nbrs.items():
                eattr['separator'] = eattr['inVars'] & eattr['outVars']
                
    def calculate_clusters(self,factor,graph,parent_seperator):
        
        localCluster = parent_seperator | set(factor.get_variables())
        
        for n in graph.neighbors(factor):
            tmpSeparator = graph[factor][n]['separator']
            localCluster = localCluster | tmpSeparator
            self.calculate_clusters(n,graph,tmpSeparator)
            
        factor.set_cluster(localCluster)

            
            
                        
        
        
            
        
        
    
