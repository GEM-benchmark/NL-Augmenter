from __future__ import annotations
from typing import List, Iterable
from tqdm import tqdm

from interfaces.Operation import Operation
from interfaces.SentenceOperation import *
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from tasks.TaskTypes import TaskType


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
Dataset for data in plain texts where each line is a datapoint
'''
class TextLineDataset(BaseDataset):
    tasks = [TaskType.TEXT_CLASSIFICATION]
    
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
        
    def __or__(self, other: TextLineDataset):
        return list(set(self.data).union(set(other.data)))

    def __and__(self, other: TextLineDataset):
        return list(set(self.data).intersection(set(other.data)))

    def __sub__(self, other: TextLineDataset):
        return list(set(self.data).difference(set(other.data)))


'''
Dataset for data in format of key-value pairs, e.g. data read from jsonl file
'''
class KeyValueDataset(BaseDataset):
    tasks = [TaskType.TEXT_TO_TEXT_GENERATION,
             TaskType.QUESTION_ANSWERING,
             TaskType.QUESTION_GENERATION]

    # data: input data samples read from jsonl file
    # task_type: task type specified
    # fields: list of relavent keys (e.g. to your sentence/target, context/question/answer, etc.)
    #         The number of keys should be aligned with the transform/filter operation.
    def __init__(self, data: List[dict], task_type=TaskType.TEXT_TO_TEXT_GENERATION, fields: List[str]=None):
        super(KeyValueDataset, self).__init__(data)
        self.task_type = task_type
        self.fields = fields
        self.operation_type = None
        
        if self.task_type == TaskType.TEXT_TO_TEXT_GENERATION:
            if len(self.fields) == 2:
                # assume two keys for SentenceAndTargetOperation, the two keys should refer to the "sentence" and "target"
                self.operation_type = "sentence_and_target"
            elif len(self.fields) > 2:
                # assume more than two keys for SentenceAndTargetsOperation, the first key refer to "sentence", others refer to "targets"
                self.operation_type = "sentence_and_targets"
        elif self.task_type in [TaskType.QUESTION_ANSWERING, TaskType.QUESTION_GENERATION]:
            self.operation_type = "question_answer"
            
        self.filter_func = self.__getattribute__(
            "_apply_" + self.operation_type + "_filter")
        self.transformation_func = self.__getattribute__(
            "_apply_" + self.operation_type + "_transformation")

    # this function is an adapter and will call the corresponding filter function for the task
    def apply_filter(self, filter: Operation):
        filtered_data = []
        print("Applying filtering:")
        for datapoint in tqdm(self.data):
            if self.filter_func(datapoint, filter):
                filtered_data.append(datapoint)
        self.data = filtered_data
        return self.data
    
    def _apply_sentence_and_target_filter(self, datapoint: dict, filter: SentenceAndTargetOperation):
        sentence = datapoint[self.fields[0]]
        target = datapoint[self.fields[1]]
        return filter.filter(sentence, target)
    
    def _apply_sentence_and_targets_filter(self, datapoint: dict, filter: SentenceAndTargetsOperation):
        sentence = datapoint[self.fields[0]]
        targets = [datapoint[target_key] for target_key in self.fields[1:]]
        return filter.filter(sentence, targets)
    
    def _apply_question_answer_filter(self, datapoint: dict, filter: QuestionAnswerOperation):
        context = datapoint[self.fields[0]]
        question = datapoint[self.fields[1]]
        answers = [datapoint[answer_key] for answer_key in self.fields[2:]]
        return filter.filter(context, question, answers)

    # this function is an adapter and will call the corresponding transform function for the task
    def apply_transformation(self, transformation: Operation):
        transformed_data = []
        print("Applying transformation:")
        for datapoint in tqdm(self.data):
            transformed_data.append(self.transformation_func(datapoint, transformation))
        self.data = transformed_data
        return self.data
    
    def _apply_sentence_and_target_transformation(self, datapoint: dict, transformation: SentenceAndTargetOperation):
        sentence = datapoint[self.fields[0]]
        target = datapoint[self.fields[1]]
        transformed_sentence, transformed_target = transformation.generate(sentence, target)
        datapoint[self.fields[0]] = transformed_sentence
        datapoint[self.fields[1]] = transformed_target
        return datapoint

    def _apply_sentence_and_targets_transformation(self, datapoint: dict, transformation: SentenceAndTargetsOperation):
        sentence = datapoint[self.fields[0]]
        targets = [datapoint[target_key] for target_key in self.fields[1:]]
        transformed_sentence, transformed_targets = transformation.generate(
            sentence, targets)
        
        datapoint[self.fields[0]] = transformed_sentence
        for i, target_key in enumerate(self.fields[1:]):
            datapoint[target_key] = transformed_targets[i]
            
        return datapoint

    def _apply_question_answer_transformation(self, datapoint: dict, transformation: QuestionAnswerOperation):
        context = datapoint[self.fields[0]]
        question = datapoint[self.fields[1]]
        answers = [datapoint[answer_key] for answer_key in self.fields[2:]]
        transformed_context, transformed_question, transformed_answers = transformation.generate(context, question, answers)
        
        datapoint[self.fields[0]] = transformed_context
        datapoint[self.fields[1]] = transformed_question
        for i, answers_key in enumerate(self.fields[2:]):
            datapoint[answers_key] = transformed_answers[i]
            
        return datapoint

    def __len__(self):
        return len(self.data)

    def _sanity_check(self, other: BaseDataset):
        assert self.data[0].keys() == other.data[0].keys(), "You cannot do dataset operation on datasets with different keys"
        assert self.task_type == other.task_type, "You cannot do dataset operation on datasets for different tasks"
        assert len(self.fields) == len(other.fields), "You cannot do dataset operation on datasets with different number fields"

    def _data2identifier(self, data: List[str]):
        id2datapoint = {}
        identifier2id = {}
        identifiers = []
        for idx, datapoint in enumerate(data):
            id2datapoint[idx] = datapoint
            # "|||" is a naive separator
            identifier = "|||".join([datapoint[field]
                                     for field in self.fields])
            identifiers.append(identifier)
            identifier2id[identifier] = idx
        identifiers = set(identifiers)  # remove duplicates
        return id2datapoint, identifier2id, identifiers
    
    def _identifier2data(self, id2datapoint, identifier2id, identifiers):
        result_data = []
        for identifier in identifiers:
            result_data.append(id2datapoint[identifier2id[identifier]])
        return result_data

    def __or__(self, other: KeyValueDataset):
        self._sanity_check(other)
        id2datapoint, identifier2id, identifiers = self._data2identifier(self.data+other.data)
        return self._identifier2data(id2datapoint, identifier2id, identifiers)
            
    def __and__(self, other: KeyValueDataset):
        self._sanity_check(other)
        id2datapoint, identifier2id, identifiers = self._data2identifier(self.data)
        _, _, identifiers2 = self._data2identifier(other.data)
        
        identifiers = identifiers.intersection(identifiers2)
        return self._identifier2data(id2datapoint, identifier2id, identifiers)

    def __sub__(self, other: KeyValueDataset):
        self._sanity_check(other)
        id2datapoint, identifier2id, identifiers = self._data2identifier(self.data)
        _, _, identifiers2 = self._data2identifier(other.data)
        
        identifiers = identifiers.difference(identifiers2)
        return self._identifier2data(id2datapoint, identifier2id, identifiers)
