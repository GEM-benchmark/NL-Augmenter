from typing import List, Iterable
from interfaces.Operation import Operation
from interfaces.SentenceOperation import SentenceOperation
from tqdm import tqdm

class BaseDataset(object):
    
    def __init__(self, data: Iterable):
        self.data = data
    
    def apply_filter(self, condition: Operation):
        raise NotImplementedError(
            "BaseDataset does not implement this function.")
        
    def apply_transformation(self, transformation: Operation):
        raise NotImplementedError(
            "BaseDataset does not implement this function.")
        
    def _get_text(self, data_row):
        raise NotImplementedError(
            "BaseDataset does not implement this function.")
        
    def __len__(self):
        raise NotImplementedError(
            "BaseDataset does not implement this function.")
    
    def __or__(self, other):
        raise NotImplementedError(
            "BaseDataset does not implement this function.")

    def __and__(self, other):
        raise NotImplementedError(
            "BaseDataset does not implement this function.")
    
    def __sub__(self, other):
        raise NotImplementedError(
            "BaseDataset does not implement this function")

'''
Dataset for data in plain texts where each line is a data example
'''
class TextLineDataset(BaseDataset):
    
    def __init__(self, data: List[str]):
        super(TextLineDataset, self).__init__(data)
        
    def apply_filter(self, filter: SentenceOperation):
        filtered_data = []
        print("Applying filtering:")
        for line in tqdm(self.data):
            if filter.filter(line):
                filtered_data.append(line)
        self.data = filtered_data
        return self.data

    def apply_transformation(self, transformation: SentenceOperation):
        transformed_data = []
        print("Applying transformation:")
        for line in tqdm(self.data):
            transformed_data.append(transformation.generate(line))
        self.data = transformed_data
        return self.data
    
    def __len__(self):
        return len(self.data)
        
    def __or__(self, other):
        return list(set(self.data).union(set(other.data)))

    def __and__(self, other):
        return list(set(self.data).intersection(set(other.data)))

    def __sub__(self, other):
        return list(set(self.data).difference(set(other.data)))


