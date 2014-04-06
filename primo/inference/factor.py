import copy
import operator

import networkx as nx

import primo.densities

class Factor(object):

    def __init__(self, node):
        self.node = node
        self.calCPD = node.get_cpd().copy()
        self.cluster = set()
        self.isEvidence = False

    def __str__(self):
        return str(self.node)

    def set_evidence(self,evd):
        self.calCPD = self.node.get_cpd().copy()
        self.calCPD = self.calCPD.set_evidence(evd)
        self.isEvidene = True

    def clear_evidence(self):
        self.calCPD = self.node.get_cpd().copy()
        self.isEvidence = False

    def set_cluster(self,cluster):
        self.cluster = cluster

    def get_variables(self):
        return self.node.get_cpd().variables

    def get_calculation_CDP(self):
        return self.calCPD;

    def get_node(self):
        return self.node

    def contains_node(self,node):
        return self.node == node

class FactorTree(object):
    '''The factor tree contains for each node of the BayesNet a factor. It
    is a directed graph with one root node. To speed up the reasoning it uses
    a message based approach which stores calculated intermediate results at
    edges. Thus, the first query is expensive and all following are easy calculated.
    The speed of the first message calculation depends on how the tree was build.
    Literature: Modeling and Reasoning with Bayesian Networks - Adnan Darwiche
    Chapter 7
    '''

    def __init__(self,graph,rootNode):
        self.graph = graph
        self.rootNode = rootNode

    def calculate_PoE(self):
        '''Calculates the probability of evidence with the set evidence'''
        if not self.graph.graph['messagesValid']:
            self.calculate_messages()
        cpd = self.calculate_marginal_forOne(self.rootNode)
        for v in cpd.get_variables()[:]:
            cpd = cpd.marginalization(v)
        return cpd

    def calculate_marginal(self,variables):
        ''' If evidence is set, then this methods calculates the posterior marginal.
        With an empty evidence this is automatically the prior marginal.'''
        if not self.graph.graph['messagesValid']:
            self.calculate_messages()
        resPT = primo.densities.ProbabilityTable.get_neutral_multiplication_PT()
        for f in self.graph.nodes():
            if f.get_node() in variables:
                resPT = resPT.multiplication(self.calculate_marginal_forOne(f))
        resPT = resPT.normalize_as_jpt()
        return resPT

    def calculate_marginal_forOne(self,factor):
        curCPD = factor.get_calculation_CDP().copy()
        for p in self.graph.predecessors(factor):
            tmpCPD = self.graph[p][factor]['msgRightWay']
            curCPD = curCPD.multiplication(tmpCPD)
        for p in self.graph.neighbors(factor):
            tmpCPD = self.graph[factor][p]['msgAgainstWay']
            curCPD = curCPD.multiplication(tmpCPD)
        for v in curCPD.get_variables()[:]:
            if v != factor.get_node():
                curCPD = curCPD.marginalization(v)
        return curCPD

    def draw(self):
        '''Draws the FactorTree'''
        import matplotlib.pyplot as plt
        nx.draw_circular(self.graph)
        plt.show()

    def calculate_messages(self):
        ''' Calculates the messages and stores the intermediate results.'''
        self.pull_phase(self.rootNode,self.graph)
        self.push_phase(self.rootNode,self.graph,primo.densities.ProbabilityTable.get_neutral_multiplication_PT())
        self.graph.graph['messagesValid'] = True

    def set_evidences(self,evidences):
        self.graph.graph['messagesValid'] = False
        evNodes = zip(*evidences)
        for factor in self.graph.nodes():
            if factor.get_node() in evNodes[0]:
                idx = evNodes[0].index(factor.get_node())
                factor.set_evidence(evidences[idx])

    def pull_phase(self,factor,graph):
        calCPD = factor.get_calculation_CDP()
        #calculate the messages of the children
        for child in graph.neighbors(factor):
            tmpInput = self.pull_phase(child,graph)
            #project each factor on the specific separator
            separator = graph[factor][child]['separator']
            for var in tmpInput.variables[:]:
                if var not in separator:
                    tmpInput = tmpInput.marginalization(var)
            #save message on edge: it's the opposite of the direction of the edge
            graph[factor][child]['msgAgainstWay'] = tmpInput
            #calculate the new message
            calCPD = calCPD.multiplication(tmpInput)
        return calCPD

    def push_phase(self,factor,graph,inCPD):
        for child in graph.neighbors(factor):
            tmpCPD = inCPD.multiplication(factor.get_calculation_CDP())
            for child2 in graph.neighbors(factor):
                if (child != child2):
                    tmpCPD = tmpCPD.multiplication(graph[factor][child2]['msgAgainstWay'])
            separator = graph[factor][child]['separator']
            #project on outgoing edge separator
            for var in tmpCPD.variables:
                if var not in separator:
                    tmpCPD = tmpCPD.marginalization(var)
            #add setOut to outgoing vars from child
            #Message with the direction of the edge
            graph[factor][child]['msgRightWay'] = tmpCPD
            self.push_phase(child,graph,tmpCPD)


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

    def create_greedy_factortree(self, bayesNet):
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
        sortNodeList = sorted(sortNodeList,key=operator.itemgetter(0),reverse=True)
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


    def find_best_node_for_insertion(self, graph, factor, nodeSet):
        '''Finds the node in the graph with the most common variables to the given node'''
        curJointCount = len(set(factor.get_variables()) & nodeSet)
        curInsertFactor = factor
        for nbs in graph.neighbors(factor):
            (count,retFactor) = self.find_best_node_for_insertion(graph,nbs,nodeSet)
            if count >= curJointCount:
                curJointCount = count
                curInsertFactor = retFactor
        return (curJointCount,curInsertFactor)


    def calculate_seperators_pull(self, factor, graph):
        s = set()
        pullSet = set(factor.get_variables())
        #find all variables in outgoing edges for factor
        for child in graph.neighbors(factor):
            s = self.calculate_seperators_pull(child,graph)
            graph[factor][child]['inVars'] =  s
            pullSet =  s | pullSet
        return pullSet

    def calculate_seperators_push(self, factor, graph, setOut):
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
        for n, nbrs in graph.adjacency_iter():
            for nbr, eattr in nbrs.items():
                eattr['separator'] = eattr['inVars'] & eattr['outVars']

    def calculate_clusters(self,factor,graph,parent_seperator):
        localCluster = parent_seperator | set(factor.get_variables())
        for n in graph.neighbors(factor):
            tmpSeparator = graph[factor][n]['separator']
            localCluster = localCluster | tmpSeparator
            self.calculate_clusters(n,graph,tmpSeparator)
        factor.set_cluster(localCluster)


class EasiestFactorElimination(object):
    '''This is the easiest way for factor elimination. It's has the worst runtime because:
    1. Needed evidences are set (optional).
    2. All nodes are multiplied.
    3. The redundant variables are summed out
    Literature: Modeling and Reasoning with Bayesian Networks - Adnan Darwiche
    Chapter 6-7
    '''
    def __init__(self, bayesNet):
        self.bn = bayesNet


    def calculate_PriorMarginal(self, variables):
        '''Calculate the prior marignal for the given variables. 
        Return the resulting CPD.'''
        nodes = self.bn.get_all_nodes()
        finCpd = nodes.pop().get_cpd()
        for n in nodes:
            finCpd = finCpd.multiplication(n.get_cpd())
        for v in finCpd.get_variables():
            if v not in variables:
                finCpd = finCpd.marginalization(v)
        return finCpd

    def calculate_PosteriorMarginal(self,variables,evidence):
        '''Calculate the posterior marginal for given variables and evidence.
        Return the resulting CPD.'''
        nodes = self.bn.get_all_nodes()
        #List of evidences
        ev_list = zip(*evidence)
        # Special Case: First Node
        node1 = nodes.pop()
        if node1 in ev_list[0]:
            ind = ev_list[0].index(node1)
            finCpd = node1.get_cpd().set_evidence(evidence[ind])
        else:
            finCpd = node1.get_cpd()
        # For all other nodes
        for n in nodes:
            if n in ev_list[0]:
                #Set evidence and multiply
                ind = ev_list[0].index(n)
                nCPD = n.get_cpd().set_evidence(evidence[ind])
                finCpd = finCpd.multiplication(nCPD)
            else:
                #only multiply
                finCpd = finCpd.multiplication(n.get_cpd())
        for v in finCpd.get_variables():
            if v not in variables:
                finCpd = finCpd.marginalization(v)
        finCpd = finCpd.normalize_as_jpt()
        return finCpd

    def calculate_PoE(self, evidence):
        ''' Calculate the probabilty of evidence for the given evidence.'''
        nodes = self.bn.get_all_nodes()
        unzipped_list = zip(*evidence)
        node1 = nodes.pop()
        if node1 in unzipped_list[0]:
            ind = unzipped_list[0].index(node1)
            finCpd = node1.get_cpd().set_evidence(evidence[ind])
        else:
            finCpd = node1.get_cpd()
        for n in nodes:
            if n in unzipped_list[0]:
                ind = unzipped_list[0].index(n)
                nCPD = n.get_cpd().set_evidence(evidence[ind])
                finCpd = finCpd.multiplication(nCPD)
            else:
                finCpd = finCpd.multiplication(n.get_cpd())
        for v in finCpd.get_variables():
            finCpd = finCpd.marginalization(v)
        return finCpd


