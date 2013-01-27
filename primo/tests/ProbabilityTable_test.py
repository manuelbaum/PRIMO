import unittest
import numpy

from primo.reasoning.density import ProbabilityTable
from primo.reasoning import DiscreteNode


class MultiplicationTest(unittest.TestCase):
    def setUp(self):
        self.pt = ProbabilityTable();

    def tearDown(self):
        self.pt = None

    def test_easy_shape(self):
        n1 = DiscreteNode("Some Node", [True, False])
        n2 = DiscreteNode("Second Node" , [True, False])

        s = n1.get_cpd().multiplication(n2.get_cpd())

        self.assertEqual(s.table.shape, (2,2));

        s = n1.get_cpd().multiplication(n1.get_cpd())
        self.assertEqual(s.table.shape,(2,))
        
    def test_easy_values(self):
        n1 = DiscreteNode("Some Node", [True, False])
        n2 = DiscreteNode("Second Node" , [True, False])
        
        cpt1 = numpy.array([2,3])
        cpt2 = numpy.array([5,7])
        
        n1.set_probability_table(cpt1,[n1])
        n2.set_probability_table(cpt2,[n2])
        
        s = n1.get_cpd().multiplication(n2.get_cpd())
        
        cptN = numpy.array([[10,14],[15,21]])
        
        numpy.testing.assert_array_equal(s.table,cptN)
        self.assertEqual(s.variables[0],n1)
        
    def test_complicated_multi(self):
        n1 = DiscreteNode("Some Node", [True, False])
        n2 = DiscreteNode("Second Node" , [True, False,"noIdea"])
        
        cpt1 = numpy.array([2,3])
        cpt2 = numpy.array([5,7,9])
        
        n1.set_probability_table(cpt1,[n1])
        n2.set_probability_table(cpt2,[n2])
        
        c3 = n1.get_cpd().multiplication(n2.get_cpd())
        c3 = n1.get_cpd().multiplication(c3)
        
        cptN = numpy.array([[20, 28, 36],[45, 63, 81]])        
        numpy.testing.assert_array_equal(c3.table,cptN)
        
class MarginalizationTest(unittest.TestCase):
    
    def test_easy_marginalize(self):
        n1 = DiscreteNode("Some Node", [True, False])
        n2 = DiscreteNode("Second Node" , [True, False, "other"])
        
        cpt1 = numpy.array([2,3])
        cpt2 = numpy.array([5,7,3])
        
        n1.set_probability_table(cpt1,[n1])
        n2.set_probability_table(cpt2,[n2])
        
        s = n1.get_cpd().multiplication(n2.get_cpd())
        s =s.marginalization(n2)
        
        print s.table
        
        cptN = numpy.array([30,45])        
        
        numpy.testing.assert_array_equal(s.table,cptN)
        self.asserEqual(s.variables[0],n1)
        
        



#include this so you can run this test without nose
if __name__ == '__main__':
    unittest.main()
