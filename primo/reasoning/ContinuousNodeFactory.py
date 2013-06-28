from primo.reasoning import ContinuousNode
from primo.reasoning.density import LinearGauss
from primo.reasoning.density import LinearExponential
from primo.reasoning.density import LinearBeta

class ContinuousNodeFactory(object):
    def __init__(self):
        pass
        
    def createLinearGaussNode(self, name):
        return self.createContinuousNode(name,(-float("Inf"),float("Inf")),LinearGauss)
        
    def createLinearExponentialNode(self, name):
        return self.createContinuousNode(name,(0,float("Inf")),LinearExponential)
        
    def createLinearBetaNode(self, name):
        return self.createContinuousNode(name,(0,1),LinearBeta)
    
    def createContinuousNode(self,name,value_range,DensityClass):
        return ContinuousNode(name,value_range,DensityClass)

