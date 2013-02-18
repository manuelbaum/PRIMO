# -*- coding: utf-8 -*-

import numpy
import operator

class UtilityTable(object):
    '''
    self.variables -- list of the parent nodes
    self.table -- utility table which contains the utility
    '''
    
    def __init__(self):
        super(UtilityTable, self).__init__()
        self.table = numpy.array(0)
        self.variables = []
    
    def add_variable(self, variable):
        self.variables.append(variable)

        ax = self.table.ndim
        self.table=numpy.expand_dims(self.table,ax)
        self.table=numpy.repeat(self.table,len(variable.value_range),axis = ax)

    def get_ut_index(self, node_value_pairs):
        nodes, values = zip(*node_value_pairs)
        index = []
        for node in self.variables:
            index_in_values_list = nodes.index(node)
            value = values[index_in_values_list]
            index.append(node.value_range.index(value))
        return tuple(index)    
        
    def set_utility_table(self, table, nodes):
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
      
    def set_utility(self, value, node_value_pairs):
        index = self.get_ut_index(node_value_pairs)
        self.table[index]=value
    
    def get_utility_table(self):
        return self.table
        
    def get_variables(self):
        return self.variables
    
    def get_utility(self, node_value_pairs):
        index = self.get_ut_index(node_value_pairs)
        return self.table[index]

    def __str__(self):
        return str(self.table)        
            
        
    
    