import random

from transformations.ChangeNamedEntities import ChangeTwoWayNamedEntities
from transformations.Transformations import TransformationsList

import unittest


class TestStringMethods(unittest.TestCase):

    def test_source_only_transformations(self):
        random.seed(0)
        transformations_list = TransformationsList()
        generations = transformations_list.generate(
            "Andrew finally returned the French book to Chris that I bought last week")
        self.assertEqual(generations['SentenceTransformation_ButterFingersPerturbation'],
                         'Andgew finally returned the French book to Chrus thav I bought last week')
        self.assertEqual(generations['SentenceTransformation_WithoutPunctuation'],
                         'Andrew finally returned the French book to Chris that I bought last week')
        self.assertEqual(generations['SentenceTransformation_BackTranslation'],
                         'Andrew finally gave the French book to Chris that I bought last week')

    def test_two_way_named_entity_replacements(self):
        tr = ChangeTwoWayNamedEntities()
        perturbed_source, perturbed_target = tr.generate("Andrew played cricket with Chris",
                                                         "Andrew seldom played cricket with Chris.")
        assert perturbed_source == "Andrew played cricket with Jacob"
        assert perturbed_target == "Andrew seldom played cricket with Jacob."


if __name__ == '__main__':
    unittest.main()
