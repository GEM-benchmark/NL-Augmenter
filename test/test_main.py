import random

from transformations.Transformations import TransformationsList

import unittest

class TestStringMethods(unittest.TestCase):

    def test_transformations(self):
        random.seed(0)
        transformationsList = TransformationsList()
        generations = transformationsList.generate(
            "Andrew finally returned the French book to Chris that I bought last week")
        self.assertEqual(generations['ButterFingersPerturbation'], 'Andgew finally returned the French book to Chrus thav I bought last week')
        self.assertEqual(generations['WithoutPunctuation'], 'Andrew finally returned the French book to Chris that I bought last week')
        # assert generations['ChangeNamedEntities'] == 'Andrew finally returned the French book to Alex that I bought last week' TODO: need to add seed here.
        self.assertEqual(generations['BackTranslation'], 'Andrew finally gave the French book to Chris that I bought last week')

    def test_numerical_transformation(self):
        random.seed(0)
        transformationsList = TransformationsList()
        generations = transformationsList.generate(
            "Andrew finally returned the five French books to Chris that contains 53.45 pages.")
        self.assertEqual(generations['ReplaceNumericalValues'],
                         'Andrew finally returned the ten French books to Chris that contains 11.13310681656804 pages.')

if __name__ == '__main__':
    unittest.main()
