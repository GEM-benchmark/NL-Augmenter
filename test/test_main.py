import random

from transformations.ChangeNamedEntities import ChangeTwoWayNamedEntities
from transformations.ReplaceNumericalValues import ReplaceNumericalValues
from transformations.Transformations import TransformationsList

import unittest


class TestStringMethods(unittest.TestCase):

    def test_source_only_transformations(self):
        random.seed(0)
        transformations_list = TransformationsList()
        generations = transformations_list.generate(
            "Andrew finally returned the French book to Chris that I bought last week")
        self.assertEqual(generations['ButterFingersPerturbation'],
                         'Andgew finally returned the French book to Chrus thav I bought last week')
        self.assertEqual(generations['WithoutPunctuation'],
                         'Andrew finally returned the French book to Chris that I bought last week')
        self.assertEqual(generations['BackTranslation'],
                         'Andrew finally gave the French book to Chris that I bought last week')
        self.assertEqual(generations['ChangeNamedEntities'],
                         'Nathaniel finally returned the French book to Chris that I bought last week')

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

    #def test_speech_perturbation(self):
        #sc = SpeechConversionError()
        #text = sc.generate("This speech conversion error needs improvement!")
        #self.assertEqual(text, "speech conversion error improvement")


if __name__ == '__main__':
    unittest.main()
