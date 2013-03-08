
import networkx as nx
import primo.reasoning.density.ProbabilityTable as ProbabilityTable
import copy



class FactorTree(object):
    
    
    def __init__(self,graph,rootNode):
        self.graph = graph
        self.rootNode = rootNode
        
    def draw(self):
        import matplotlib.pyplot as plt
        nx.draw_circular(self.graph)
        plt.show()
        
        
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

        #add local vars to set
        calCPD = inCPD.copy()
        

        for child in graph.neighbors(factor):
            tmpCPD = calCPD
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
            
    
    
    
    
