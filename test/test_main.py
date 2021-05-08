import random
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from transformations.change_named_entities.transformation import ChangeTwoWayNamedEntities
from transformations.replace_numerical_values.transformation import ReplaceNumericalValues
from Transformations import *

import unittest


class TestStringMethods(unittest.TestCase):

    def test_jsons(self):
        execute_test_cases()

    def test_two_way_named_entity_replacements(self):
        tr = ChangeTwoWayNamedEntities()
        perturbed_source, perturbed_target = tr.generate("Andrew played cricket with Chris",
                                                         "Andrew seldom played cricket with Chris.")
        assert perturbed_source == "Andrew played cricket with Jacob"
        assert perturbed_target == "Andrew seldom played cricket with Jacob."
        perturbed_source, perturbed_target = tr.generate("Andrew played cricket in India",
                                                         "India was the country where Jonathan played.")
        assert perturbed_source == "Andrew played cricket in Canada"
        assert perturbed_target == "Canada was the country where Jonathan played."

    def test_numerical_transformation(self):
        random.seed(10)
        perturber = ReplaceNumericalValues()
        transformed = perturber.generate(
            "Andrew finally returned the five French books to Chris that contains 53.45 pages.")
        self.assertEqual(transformed,
                         'Andrew finally returned the nine French books to Chris that contains 3.26 pages.')


if __name__ == '__main__':
    unittest.main()
