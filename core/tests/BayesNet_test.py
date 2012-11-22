import unittest

from core.BayesNet import BayesNet
from core.Node import Node


class NodeAddAndRemoveTestCase(unittest.TestCase):
    def setUp(self):
        self.bn = BayesNet()

    def tearDown(self):
        self.bn = None

    def test_add_node(self):
        n = Node("Some Node")
        self.bn.add_node(n)
        self.assertEqual(n, self.bn.get_node("Some Node"))
        self.assertTrue(n in self.bn.get_nodes(["Some Node"]))

        node_with_same_name = Node("Some Node")
        self.assertRaises(Exception, self.bn.add_node, node_with_same_name)

    def test_remove_node(self):
        n = Node("Some Node to remove")
        self.bn.add_node(n)
        self.bn.remove_node(n)
        self.assertFalse(n in self.bn.get_nodes([]))

    def test_add_edge(self):
        n1 = Node("1")
        n2 = Node("2")
        self.bn.add_node(n1)
        self.bn.add_node(n2)
        self.bn.add_edge(n1, n2)
        self.assertTrue(n1 in self.bn.get_parents(n2))
        self.assertTrue(n2 in self.bn.get_children(n1))
        self.bn.remove_node(n1)
        self.bn.remove_node(n2)

    def test_remove_edge(self):
        n1 = Node("1")
        n2 = Node("2")
        self.bn.add_node(n1)
        self.bn.add_node(n2)
        self.bn.add_edge(n1, n2)
        self.bn.remove_edge(n1, n2)
        self.assertEqual([], self.bn.get_parents(n2))
        self.bn.remove_node(n1)
        self.bn.remove_node(n2)

#include this so you can run this test without nose
if __name__ == '__main__':
    unittest.main()
