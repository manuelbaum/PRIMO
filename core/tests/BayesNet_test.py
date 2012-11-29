import unittest

from core.BayesNet import BayesNet
from reasoning.DiscreteNode import DiscreteNode


class NodeAddAndRemoveTestCase(unittest.TestCase):
    def setUp(self):
        self.bn = BayesNet()

    def tearDown(self):
        self.bn = None

    def test_clear_and_len(self):
        self.assertFalse(0 == len(self.bn))
        self.assertFalse(0 == self.bn.number_of_nodes())
        self.bn.clear()
        self.assertEqual(0, len(self.bn))
        self.assertEqual(0, self.bn.number_of_nodes())

    def test_add_node(self):
        self.bn.clear()
        n = DiscreteNode("Some Node", [True, False])
        self.bn.add_node(n)
        self.assertEqual(n, self.bn.get_node("Some Node"))
        self.assertTrue(n in self.bn.get_nodes(["Some Node"]))
        node_with_same_name = DiscreteNode("Some Node", [True, False])
        self.assertRaises(Exception, self.bn.add_node, node_with_same_name)

    def test_remove_node(self):
        self.bn.clear()
        n = DiscreteNode("Some Node to remove", [True, False])
        self.bn.add_node(n)
        self.bn.remove_node(n)
        self.assertFalse(n in self.bn.get_nodes([]))

    def test_add_edge(self):
        self.bn.clear()
        n1 = DiscreteNode("1", [True, False])
        n2 = DiscreteNode("2", [True, False])
        self.bn.add_node(n1)
        self.bn.add_node(n2)
        self.bn.add_edge(n1, n2)
        self.assertTrue(n1 in self.bn.get_parents(n2))
        self.assertTrue(n2 in self.bn.get_children(n1))

    def test_remove_edge(self):
        self.bn.clear()
        n1 = DiscreteNode("1", [True, False])
        n2 = DiscreteNode("2", [True, False])
        self.bn.add_node(n1)
        self.bn.add_node(n2)
        self.bn.add_edge(n1, n2)
        self.assertEqual([n1], self.bn.get_parents(n2))
        self.bn.remove_edge(n1, n2)
        self.assertEqual([], self.bn.get_parents(n2))

    def test_is_valid(self):
        self.bn.clear()
        n1 = DiscreteNode("1", [True, False])
        n2 = DiscreteNode("2", [True, False])
        self.bn.add_node(n1)
        self.bn.add_node(n2)
        self.bn.add_edge(n1, n2)
        self.assertTrue(self.bn.is_valid())
        self.bn.add_edge(n1, n1)
        self.assertFalse(self.bn.is_valid())
        self.bn.remove_edge(n1, n1)
        self.assertTrue(self.bn.is_valid())
        n3 = DiscreteNode("3", [True, False])
        n4 = DiscreteNode("4", [True, False])
        self.bn.add_node(n3)
        self.bn.add_node(n4)
        self.assertTrue(self.bn.is_valid())
        self.bn.add_edge(n2, n3)
        self.assertTrue(self.bn.is_valid())
        self.bn.add_edge(n3, n4)
        self.assertTrue(self.bn.is_valid())
        self.bn.add_edge(n4, n1)
        self.assertFalse(self.bn.is_valid())


#include this so you can run this test without nose
if __name__ == '__main__':
    unittest.main()
