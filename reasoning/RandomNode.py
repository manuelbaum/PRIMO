# -*- coding: utf-8 -*-

from core.Node import Node
from reasoning.CPD import CPD


class AbstractRandomNode(Node):
    '''TODO: write doc'''

    cpd = CPD()

    def __init__(self):
        super(AbstractRandomNode, self).__init__()