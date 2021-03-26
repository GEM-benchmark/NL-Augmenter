import random

from common.webnlg.DataEntry import DataEntry
from data_transformations.DataTransformation import DataTransformation
from common.NumericalTransformation import NumericalTransformation


class ReplaceDataNumericalValues(DataTransformation):

    numerical_transformation = None

    def __init__(self):
        self.numerical_transformation = NumericalTransformation()

    def generate(self, dataset: object, data_subset: str, dataset_size=None):
        if isinstance(dataset, dict):
            input_obj_list = []

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
                input_obj_list.append(input_object)

            # Convert Back to dataset representation:
            dataset_list = []
            if dataset_size and isinstance(dataset_size, int):
                sample_input_list = random.sample(input_obj_list, dataset_size)
                dataset_list = [a_data_entry.generate_entry_dict() for a_data_entry in sample_input_list]
            else:
                dataset_list = [a_data_entry.generate_entry_dict() for a_data_entry in input_obj_list]

            return {
                data_subset: dataset_list
            }

        return None


