# -*- coding: utf-8 -*-
import numpy
from reasoning.CPD import CPD

class CPT(CPD):
    '''TODO: write doc'''

    

    def __init__(self, owner):
        super(CPT, self).__init__()
        
        self.owner = owner
        self.variables = [owner]

        size_of_range = len(owner.value_range)
        self.values = numpy.ones(size_of_range) / size_of_range

    def add_parent(self, parent):
        self.variables.append(parent)

        ax = self.values.ndim
        self.values=numpy.expand_dims(self.values,ax)
        self.values=numpy.repeat(self.values,len(parent.value_range),axis = ax)   

    def set_probability(self, value, node_value_pairs):
        index = self.get_cpt_index(node_value_pairs) 
        self.values[tuple(index)]=value

    def get_cpt_index(self, node_value_pairs):
        nodes, values = zip(*node_value_pairs)
        index = []
        for node in self.variables:
            index_in_values_list = nodes.index(node)
            value = values[index_in_values_list]
            index.append(node.value_range.index(value))
        return index
                    


    def multiplication(self, factor):
        raise Exception("Called unimplemented function")    
    
    def marginalization(self, value_name):
        raise Exception("Called unimplemented function")

    def reduction(self):
        raise Exception("Called unimplemented function")

    def division(self, factor):
        raise Exception("Called unimplemented function")

    def __str__(self):
        return str(self.values)
