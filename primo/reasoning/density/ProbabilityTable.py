# -*- coding: utf-8 -*-
import numpy
import copy
from primo.reasoning.density import Density

class ProbabilityTable(Density):
    '''TODO: write doc'''

    

    def __init__(self):
        super(ProbabilityTable, self).__init__()
        
        #self.owner = owner
        #self.variables = [owner]

        #size_of_range = len(owner.value_range)
        #self.table = numpy.ones(size_of_range) / size_of_range

        self.variables = []
        self.table = numpy.array(0)

    def add_variable(self, variable):
        self.variables.append(variable)

        ax = self.table.ndim
        self.table=numpy.expand_dims(self.table,ax)
        self.table=numpy.repeat(self.table,len(variable.value_range),axis = ax)   

    def set_probability_table(self, table, nodes):
        if not set(nodes) == set(self.variables):
            raise Exception("The list which should define the ordering of the variables does not match"
                " the variables that this cpt depends on (plus the node itself)")
        if not self.table.ndim == table.ndim:
            raise Exception("The provided probability table does not have the right number of dimensions")
        for d,node in enumerate(nodes):
            if len(node.value_range) != table.shape[d]:
                raise Exception("The size of the provided probability table does not match the number of possible values of the node "+node.name+" in dimension "+str(d))

        self.table = table
        self.variables = nodes

    def set_probability(self, value, node_value_pairs):
        index = self.get_cpt_index(node_value_pairs) 
        self.table[tuple(index)]=value

    def get_cpt_index(self, node_value_pairs):
        nodes, values = zip(*node_value_pairs)
        index = []
        for node in self.variables:
            index_in_values_list = nodes.index(node)
            value = values[index_in_values_list]
            index.append(node.value_range.index(value))
        return index


    def is_normalized_as_cpt(self,owner):

        dim_of_owner = self.variables.index(owner)
        sum_of_owner_probs = numpy.sum(self.table, dim_of_owner)

        return set(sum_of_owner_probs.flatten()) == set([1])

    def is_normalized_as_jpt(self):
        return numpy.sum(table) == 1.0

    def multiplication(self, factor):
        raise Exception("Called unimplemented function")    
    
    def marginalization(self, variable):
        raise Exception("Called unimplemented function")       
        
    def reduction(self, evidence):
        '''Returns a reduced version of this ProbabilityTable, evidence is a list of pairs.
            Important: This node is not being changed!'''
        reduced = ProbabilityTable()
        reduced.variables = copy.copy(self.variables)
        reduced.table = self.table
        for node,value in evidence:

            axis=reduced.variables.index(node)
            position=node.value_range.index(value)
            reduced.table = numpy.take(reduced.table,[position],axis=axis)
            
            reduced.table=reduced.table.squeeze()
            reduced.variables.remove(node)
            
        return reduced
            
            

    def division(self, factor):
        raise Exception("Called unimplemented function")

    def __str__(self):
        return str(self.table)
