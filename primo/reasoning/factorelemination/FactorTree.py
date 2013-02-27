
import networkx as nx



class FactorTree(object):
    
    
    def __init__(self,graph,rootNode):
        self.graph = graph
        self.rootNode = rootNode
        
    def draw(self):
        import matplotlib.pyplot as plt
        nx.draw_circular(self.graph)
        plt.show()
            
    
    
    
    
