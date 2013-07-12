from primo.reasoning import ContinuousNode
from primo.reasoning.density import Gauss
from primo.reasoning.density import Exponential
from primo.reasoning.density import Beta

class ContinuousNodeFactory(object):
    '''This class offers methods for generating ContinuousNodes'''
    def __init__(self):
        pass
        
    def createGaussNode(self, name):
        '''
        Create a LinearGaussNode with linear dependencies on parents.
        
        @param name: The name of the node.
        '''        
        return self.createContinuousNode(name,(-float("Inf"),float("Inf")),Gauss)
        
    def createExponentialNode(self, name):
        '''
        Create a LinearExponentialNode with linear dependencies on parents.
        
        @param name: The name of the node.
        '''  
        return self.createContinuousNode(name,(0,float("Inf")),Exponential)
        
    def createBetaNode(self, name):
        '''
        Create a LinearBetaNode with linear dependencies on parents.
        
        @param name: The name of the node.
        '''  
        return self.createContinuousNode(name,(0,1),Beta)
    
    def createContinuousNode(self,name,value_range,DensityClass):
        '''
        Create a ContinuousNode. This method should only be invoked from
        outside this class if no specialized method is available.
        
        @param name: The name of the node.
        @param value_range: A 2-tuple which represents the interval that is the
            domain of the variable.
        @param DensityClass: A class from primo.reasoning.density that shall be
            the node's pdf
        '''  
        return ContinuousNode(name,value_range,DensityClass)

