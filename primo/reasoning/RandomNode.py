# -*- coding: utf-8 -*-

from primo.core import Node
from primo.reasoning.density import Density


class RandomNode(Node):
    '''TODO: write doc'''

    cpd = Density()

    def __init__(self, name):
        super(RandomNode, self).__init__(name)

    def is_valid(self):
        raise Exception("Called an unimplemented function")
        
