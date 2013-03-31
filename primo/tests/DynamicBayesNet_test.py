# -*- coding: utf-8 -*-
import unittest

from primo.core import DynamicBayesNet
from primo.reasoning import DiscreteNode


class DynamicBayesNetTest(unittest.TestCase):
    def setUp(self):
        self.dbn = DynamicBayesNet()

    def tearDown(self):
        self.dbn = None

    def test_add_node(self):
        self.dbn.clear()
        n = DiscreteNode("Some Node", [True, False])
        self.dbn.add_node(n)
        self.assertEqual(n, self.dbn.get_node("Some Node"))
        self.assertTrue(n in self.dbn.get_nodes(["Some Node"]))

    def test_temporal_edges(self):
        self.dbn.clear()
        n1 = DiscreteNode("1", [True, False])
        n2 = DiscreteNode("2", [False, False])
        self.dbn.add_node(n1)
        self.dbn.add_node(n2)
        self.assertTrue(self.dbn.is_valid())
        self.dbn.add_edge(n1, n1)
        self.assertFalse(self.dbn.is_valid())
        self.dbn.add_edge(n1, n1, True)
        self.assertTrue(self.dbn.is_valid())


#include this so you can run this test without nose
if __name__ == '__main__':
    unittest.main()
