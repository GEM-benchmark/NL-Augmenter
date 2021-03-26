from data_transformations.DataTransformationList import DataTransformationList
from datasets import load_dataset

import unittest


class TestDataMethods(unittest.TestCase):

    def test_data_transformation_no_dataset(self):
        transformation_list = DataTransformationList()
        generations = transformation_list.generate(None, "None")

        self.assertIsNone(generations["ReplaceDataNumericalValues"])

    def test_data_numerical_webnlg_validation_dataset(self):
        transformation_list = DataTransformationList()
        dataset = load_dataset('gem', 'web_nlg_en')
        generations = transformation_list.generate(dataset, "validation")

        self.assertIsNotNone(generations["ReplaceDataNumericalValues"])
        self.assertIsNotNone(generations["ReplaceDataNumericalValues"]["validation"])

    def test_data_numerical_webnlg_test_dataset(self):
        transformation_list = DataTransformationList()
        dataset = load_dataset('gem', 'web_nlg_en')
        generations = transformation_list.generate(dataset, "test")

        self.assertIsNotNone(generations["ReplaceDataNumericalValues"])
        self.assertIsNotNone(generations["ReplaceDataNumericalValues"]["test"])

    def test_limited_data_numerical_webnlg_test_dataset(self):
        transformation_list = DataTransformationList()
        dataset = load_dataset('gem', 'web_nlg_en')
        generations = transformation_list.generate(dataset, "test", 5)

        self.assertIsNotNone(generations["ReplaceDataNumericalValues"])
        self.assertIsNotNone(generations["ReplaceDataNumericalValues"]["test"])
        self.assertEqual(5, len(generations["ReplaceDataNumericalValues"]["test"]))
