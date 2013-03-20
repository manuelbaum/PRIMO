
import networkx as nx
import primo.reasoning.density.ProbabilityTable as ProbabilityTable



class FactorTree(object):
    
    
    def __init__(self,graph,rootNode):
        self.graph = graph
        self.rootNode = rootNode
        self.graph['messagesValid'] = False
        
    def calculate_marginal(self,variables):
        if not self.graph['messagesValid']:
            self.calculateMessages()
            
        resPT = ProbabilityTable()
            
        for f in self.graph.nodes():
            if f.get_node() in variables:
                resPT = resPT.multiplication.calculate_marginal_forOne(f)
                
        return resPT
                
    def calculate_marginal_forOne(self,factor):
        curCPD = factor.get_calculation_CDP().copy()
        for p in self.graph.predecessors(factor):
            curCPD = curCPD.multiplication(self.graph[p][factor]['inMessage'])
            
        for p in self.graph.neighbors(factor):
            curCPD = curCPD.multiplication(self.graph[factor][p]['outMessage'])
            
        for v in curCPD.get_variables()[:]:
            if v != factor.get_node():
                curCPD = curCPD.marginalization(v)
                
        return curCPD
        
        
    def draw(self):
        import matplotlib.pyplot as plt
        nx.draw_circular(self.graph)
        plt.show()
        
    def calculateMessages(self):
        self.push_phase(self.rootNode,self.graph)
        self.pull_phase(self.rootNode,self.graph,ProbabilityTable())
        self.graph['messagesValid'] = True
        
        
    def setEvidences(self,evidences):
        self.graph['messagesValid'] = False
        
        evNodes = zip(*evidences)        
        
        for factor in self.graph.get_all_nodes():
            if factor.get_node() in evNodes:
                idx = evNodes.index(factor.get_node())
                factor.set_evidence(evidences[idx])
        
    
        
        
    def pull_phase(self,factor,graph):
        
        calCPD = factor.get_calculate_CPD()
        #calculate the messages of the children
        for child in graph.neighbors(factor):
            tmpInput = self.pull_phase(child,graph)
            #project each factor on the specific seperator
            seperator = graph[factor][child]['seperator']
            for var in tmpInput.variables[:]:
                if var not in seperator:
                    tmpInput = tmpInput.marginalization(var)
                
            #save message on edge
            graph[factor][child]['inMessage'] = tmpInput
            #calculate the new message
            calCPD = calCPD.multiplication(tmpInput)
              
        return calCPD
        
    def push_phase(self,factor,graph,inCPD):
       

        for child in graph.neighbors(factor):
            tmpCPD = inCPD.copy()
            for child2 in graph.neighbors(factor):
                if (child != child2):
                    tmpCPD = tmpCPD.multiplication(graph[factor][child2]['inMessage'])
            
            seperator = graph[factor][child]['seperator']
            #project on outgoing edge seperator
            for var in tmpCPD.variables[:]:
                if var not in seperator:
                    tmpCPD = tmpCPD.marginalization(var)
            
            #add setOut to outgoing vars from child
            graph[factor][child]['outMessage'] = tmpCPD
                
           
            self.push_phase(child,graph,tmpCPD)
            
    
    
    
    
