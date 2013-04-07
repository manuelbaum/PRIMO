
import networkx as nx
import primo.reasoning.density.ProbabilityTable as ProbabilityTable


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
            
            
        resPT = ProbabilityTable.get_neutral_multiplication_PT()
        
            
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
        self.push_phase(self.rootNode,self.graph,ProbabilityTable.get_neutral_multiplication_PT())
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
            
    
    
    
    
