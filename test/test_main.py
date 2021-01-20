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

if __name__ == '__main__':
    unittest.main()
