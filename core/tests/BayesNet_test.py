import unittest

from core.BayesNet import BayesNet
from core.Node import Node


class NodeAddAndRemoveTestCase(unittest.TestCase):
    def setUp(self):
        self.bn = BayesNet()

    def tearDown(self):
        self.bn = None

    def test_add(self):
        n = Node("Some Node")
        self.bn.add_node(n)
        self.assertEqual(n, self.bn.get_node("Some Node"))
        self.assertTrue(n in self.bn.get_nodes(["Some Node"]))

        node_with_same_name = Node("Some Node")
        self.assertRaises(Exception, self.bn.add_node, node_with_same_name)

    def test_remove(self):
        n = Node("Some Node to remove")
        self.bn.add_node(n)
        self.bn.remove_node(n)
        self.assertFalse(n in self.bn.get_nodes())


#include this so you can run this test without nose
if __name__ == '__main__':
    unittest.main()
