import unittest

from primo.utils import XMLBIF
from primo.core import BayesNet
from primo.reasoning import DiscreteNode
import numpy
import os

class ImportExportTest(unittest.TestCase):
    def setUp(self):
        # Create BayesNet
        self.bn = BayesNet();
        # Create Nodes
        weather0 = DiscreteNode("Weather0", ["Sun", "Rain"])
        weather = DiscreteNode("Weather", ["Sun", "Rain"])
        ice_cream_eaten = DiscreteNode("Ice Cream Eaten", [True, False])
        # Add nodes
        self.bn.add_node(weather0)
        self.bn.add_node(weather)
        self.bn.add_node(ice_cream_eaten)
        # Add edges
        self.bn.add_edge(weather, ice_cream_eaten)
        self.bn.add_edge(weather0, weather);
        # Set probabilities
        cpt_weather0 = numpy.array([.6, .4])
        weather0.set_probability_table(cpt_weather0, [weather0])
        cpt_weather = numpy.array([[.7, .5],
                                   [.3, .5]])
        weather.set_probability_table(cpt_weather, [weather0, weather])
        ice_cream_eaten.set_probability(.9, [(ice_cream_eaten, True), (weather, "Sun")])
        ice_cream_eaten.set_probability(.1, [(ice_cream_eaten, False), (weather, "Sun")])
        ice_cream_eaten.set_probability(.2, [(ice_cream_eaten, True), (weather, "Rain")])
        ice_cream_eaten.set_probability(.8, [(ice_cream_eaten, False), (weather, "Rain")])
    
    def test_import_export(self):
        # write BN 
        xmlbif = XMLBIF(self.bn, "Test Net")
        xmlbif.write("test_out.xmlbif")
        # read BN
        bn2 = XMLBIF.read("test_out.xmlbif")
        for node1 in self.bn.get_nodes():
            
            name_found = False
            cpd_equal = False
            value_range_equal = False
            str_equal = False
            pos_equal = False
            for node2 in bn2.get_nodes():
                # Test node names
                if node1.name == node2.name:
                    name_found = True
                    cpd_equal = node1.get_cpd == node2.get_cpd
                    value_range_equal = node1.get_value_range() == node2.get_value_range()
                    str_equal = str(node1) == str(node2)
                    pos_equal = node1.pos == node2.pos
            self.assertTrue(name_found)
            self.assertTrue(cpd_equal)
            self.assertTrue(value_range_equal)
            self.assertTrue(str_equal)
            self.assertTrue(pos_equal)
        # remove file
        os.remove("test_out.xmlbif")
        

#include this so you can run this test without nose
if __name__ == '__main__':
    unittest.main()
