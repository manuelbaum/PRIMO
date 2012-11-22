# -*- coding: utf-8 -*-

from core.Node import Node
from reasoning.CPD import CPD


class RandomNode(Node):
    '''TODO: write doc'''

    cpd = CPD()

    def __init__(self, name):
        super(RandomNode, self).__init__(name)
        
