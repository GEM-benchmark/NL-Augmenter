from common.webnlg.DataEntry import DataEntry
from data_transformations.DataTransformation import DataTransformation
from common.NumericalTransformation import NumericalTransformation


class ReplaceDataNumericalValues(DataTransformation):

    numerical_transformation = None

    def __init__(self):
        self.numerical_transformation = NumericalTransformation()

    def generate(self, dataset: object, data_subset: str):
        if isinstance(dataset, dict):

            # dict where the key is a category and the value is a list which will contain
            # all DataEntry objects of that category:
            input_objects_per_category = {}
            # dict where the key is a category and the value is a dict in which the key is the input size
            # and the value a list which will contain all DataEntry objects of that category
            input_objects_per_category_per_size = {}

            for index in range(len(dataset[data_subset])):
                # Replace Numerical Values:
                input_triple_list = dataset[data_subset][index]['input']
                for triple_index, line_triple in enumerate(input_triple_list):
                    triple_split_list = line_triple.split(' | ')

                    for triple_token_index, triple_token in enumerate(triple_split_list):
                        triple_split_list[triple_token_index] = self.numerical_transformation.transform(triple_token)

                    input_triple = ' | '.join(triple_split_list)
                    input_triple_list[triple_index] = input_triple

                target = self.numerical_transformation.transform(dataset[data_subset][index]['target'])

                input_object = DataEntry(dataset[data_subset][index]['gem_id'], dataset[data_subset][index]['category'],
                                         input_triple_list, dataset[data_subset][index]['references'],
                                         target, dataset[data_subset][index]['webnlg_id'])

                # if the current category is not found in the dict, create a key with the category label in the dict
                if not input_object.category in input_objects_per_category:
                    input_objects_per_category[input_object.category] = []
                input_objects_per_category[input_object.category].append(input_object)

                # if the current category is not found in the dict, create a key with the category label in the dict
                if not input_object.category in input_objects_per_category_per_size:
                    input_objects_per_category_per_size[input_object.category] = {}
                # if the current input size is not found in the dict,
                # create a key with the input size number label in the embedded dict
                if not input_object.input_size in input_objects_per_category_per_size[input_object.category]:
                    input_objects_per_category_per_size[input_object.category][input_object.input_size] = []
                input_objects_per_category_per_size[input_object.category][input_object.input_size].append(
                    input_object)

            return {
                "input_objects_per_category": input_objects_per_category,
                "input_objects_per_category_per_size": input_objects_per_category_per_size
            }

        return None


