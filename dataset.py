from __future__ import annotations
from typing import List, Iterable
from tqdm import tqdm

from interfaces.SentenceOperation import *
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from tasks.TaskTypes import TaskType


class BaseDataset(Iterable):
    def __init__(self, data: Iterable):
        self.data = data

    def apply_filter(self, condition: Operation):
        raise NotImplementedError("BaseDataset does not implement this function.")

    def apply_transformation(self, transformation: Operation):
        raise NotImplementedError("BaseDataset does not implement this function.")

    def __iter__(self):
        raise NotImplementedError("BaseDataset does not implement this function.")

    def __len__(self):
        raise NotImplementedError("BaseDataset does not implement this function.")

    def __or__(self, other):
        raise NotImplementedError("BaseDataset does not implement this function.")

    def __and__(self, other):
        raise NotImplementedError("BaseDataset does not implement this function.")

    def __sub__(self, other):
        raise NotImplementedError("BaseDataset does not implement this function")


"""
Dataset for data in plain texts where each line is a datapoint
"""


class TextLineDataset(BaseDataset):
    tasks = [TaskType.TEXT_CLASSIFICATION]

    def __init__(self, data: List[str], labels: List):
        super(TextLineDataset, self).__init__(data)
        assert len(data) == len(
            labels
        ), "The number of datapoint should be the same as the number of labels"
        self.labels = labels
        self.mapping = {
            datapoint: label for datapoint, label in zip(self.data, self.labels)
        }

    @classmethod
    def from_huggingface(cls, dataset, fields):
        data = []
        labels = []
        for example in dataset:
            data.append(example[fields[0]])
            labels.append(example[fields[1]])
        return cls(data, labels)

    def apply_filter(self, filter: SentenceOperation) -> TextLineDataset:
        filtered_data = []
        filtered_labels = []
        print("Applying filtering:")
        for datapoint, label in tqdm(zip(self.data, self.labels), total=len(self.data)):
            if filter.filter(datapoint):
                filtered_data.append(datapoint)
                filtered_labels.append(label)

        return TextLineDataset(filtered_data, filtered_labels)

    def apply_transformation(
            self, transformation: SentenceOperation
    ) -> TextLineDataset:
        transformed_data = []
        print("Applying transformation:")
        for line in tqdm(self.data):
            transformed_data.extend(transformation.generate(line))

        return TextLineDataset(transformed_data, self.labels)

    def __iter__(self):
        for text, label in zip(self.data, self.labels):
            yield (text, label)

    def __len__(self):
        return len(self.data)

    def __or__(self, other: TextLineDataset) -> TextLineDataset:
        data = list(set(self.data).union(set(other.data)))
        mapping = {**self.mapping, **other.mapping}
        labels = [mapping[datapoint] for datapoint in data]
        return TextLineDataset(data, labels)

    def __and__(self, other: TextLineDataset) -> TextLineDataset:
        data = list(set(self.data).intersection(set(other.data)))
        labels = [self.mapping[datapoint] for datapoint in data]
        return TextLineDataset(data, labels)

    def __sub__(self, other: TextLineDataset) -> TextLineDataset:
        data = list(set(self.data).difference(set(other.data)))
        labels = [self.mapping[datapoint] for datapoint in data]
        return TextLineDataset(data, labels)


"""
Dataset for data in format of key-value pairs, e.g. data read from jsonl file
"""


class KeyValueDataset(BaseDataset):
    tasks = [
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.QUESTION_ANSWERING,
        TaskType.QUESTION_GENERATION,
    ]

    # data: input data samples read from jsonl file
    # task_type: task type specified
    # fields: list of relavent keys (e.g. to your sentence/target, context/question/answer, etc.)
    #         The number of keys should be aligned with the transform/filter operation.
    def __init__(
            self,
            data: List[dict],
            task_type=TaskType.TEXT_TO_TEXT_GENERATION,
            fields: List[str] = None,
    ):
        super(KeyValueDataset, self).__init__(data)
        self.task_type = task_type
        self.fields = fields
        self.operation_type = None

    @classmethod
    def from_huggingface(cls, dataset, task_type, fields):
        data = []
        if task_type not in [TaskType.QUESTION_ANSWERING, TaskType.QUESTION_GENERATION]:
            for example in dataset:
                data.append({key: example[key] for key in fields})
        else:
            # this is an ugly implementation, which hard-codes the squad data format
            # TODO might need a more elegant way to deal with the fields with hierachy, e.g. the answers field in squad data (exampl['answers']['text'])
            for example in dataset:
                data.append(
                    {
                        fields[0]: example[fields[0]],
                        fields[1]: example[fields[1]],
                        fields[2]: example[fields[2]]["text"],
                    }
                )
        return cls(data, task_type, fields)

    def _analyze(self, subfields: List[str]):
        if subfields is None:
            subfields = self.fields

        assert set(subfields) <= set(
            self.fields
        ), "Your can only choose from fields within {}".format(self.fields)

        if self.task_type == TaskType.TEXT_TO_TEXT_GENERATION:
            if len(subfields) == 1:
                self.operation_type = "sentence"
            elif len(subfields) == 2:
                self.operation_type = "sentence_and_target"
            elif len(subfields) > 2:
                self.operation_type = "sentence_and_targets"
        elif self.task_type in [
            TaskType.QUESTION_ANSWERING,
            TaskType.QUESTION_GENERATION,
        ]:
            # this is in case that one would like to use SentenceOperation (e.g. butter finger) on specific fields (e.g. only the question)
            if len(subfields) == 1:
                self.operation_type = "sentence"
            elif len(subfields) == 2:
                self.operation_type = "sentence_and_target"
            else:
                self.operation_type = "question_answer"

        filter_func = self.__getattribute__("_apply_" + self.operation_type + "_filter")
        transformation_func = self.__getattribute__(
            "_apply_" + self.operation_type + "_transformation"
        )
        return filter_func, transformation_func

    # this function is an adapter and will call the corresponding filter function for the task
    # subfields: the fields to apply filter, it is a subset of self.fields
    def apply_filter(
            self, filter: Operation, subfields: List[str] = None
    ) -> KeyValueDataset:
        filter_func, _ = self._analyze(subfields)

        filtered_data = []
        print("Applying filtering:")
        for datapoint in tqdm(self.data):
            if filter_func(datapoint, filter):
                filtered_data.append(datapoint)

        return KeyValueDataset(filtered_data, self.task_type, self.fields)

    def _apply_sentence_filter(self, datapoint: dict, filter: SentenceOperation):
        sentence = datapoint[self.fields[0]]
        return filter.filter(sentence)

    def _apply_sentence_and_target_filter(
            self, datapoint: dict, filter: SentenceAndTargetOperation
    ):
        sentence = datapoint[self.fields[0]]
        target = datapoint[self.fields[1]]
        return filter.filter(sentence, target)

    def _apply_sentence_and_targets_filter(
            self, datapoint: dict, filter: SentenceAndTargetsOperation
    ):
        sentence = datapoint[self.fields[0]]
        targets = [datapoint[target_key] for target_key in self.fields[1:]]
        return filter.filter(sentence, targets)

    def _apply_question_answer_filter(
            self, datapoint: dict, filter: QuestionAnswerOperation
    ):
        context = datapoint[self.fields[0]]
        question = datapoint[self.fields[1]]
        answers = [datapoint[answer_key] for answer_key in self.fields[2:]]
        return filter.filter(context, question, answers)

    # this function is an adapter and will call the corresponding transform function for the task
    # subfields: the fields to apply transformation, it is a subset of self.fields
    def apply_transformation(
            self, transformation: Operation, subfields: List[str] = None
    ) -> KeyValueDataset:
        _, transformation_func = self._analyze(subfields)
        transformed_data = []
        print("Applying transformation:")
        for datapoint in tqdm(self.data):
            transformed_data.extend(
                transformation_func(datapoint.copy(), transformation)
            )  # don't want self.data to be changed

        return KeyValueDataset(transformed_data, self.task_type, self.fields)

    def _apply_sentence_transformation(
            self, datapoint: dict, transformation: SentenceOperation
    ):
        sentence = datapoint[self.fields[0]]
        transformed_sentence = transformation.generate(sentence)
        datapoint[self.fields[0]] = transformed_sentence
        return [datapoint]

    def _apply_sentence_and_target_transformation(
            self, datapoint: dict, transformation: SentenceAndTargetOperation
    ):
        sentence = datapoint[self.fields[0]]
        target = datapoint[self.fields[1]]
        transformed_sentence, transformed_target = transformation.generate(
            sentence, target
        )
        datapoint[self.fields[0]] = transformed_sentence
        datapoint[self.fields[1]] = transformed_target
        return [datapoint]

    def _apply_sentence_and_targets_transformation(
            self, datapoint: dict, transformation: SentenceAndTargetsOperation
    ):
        sentence = datapoint[self.fields[0]]
        targets = [datapoint[target_key] for target_key in self.fields[1:]]
        transformed = transformation.generate(
            sentence, targets
        )
        datapoints = []
        for to in transformed:
            datapoint_n = dict()
            datapoint_n[self.fields[0]] = to[0]
            for i, target_key in enumerate(self.fields[1:]):
                datapoint[target_key] = to[1][1+i] # targets starting from pos 1
            datapoints.append(datapoint_n)
        return datapoints

    def _apply_question_answer_transformation(
            self, datapoint: dict, transformation: QuestionAnswerOperation
    ):
        context = datapoint[self.fields[0]]
        question = datapoint[self.fields[1]]
        answers = [datapoint[answer_key] for answer_key in self.fields[2:]]
        transformed = transformation.generate(context, question, answers)

        datapoints = []
        for to in transformed:
            datapoint_n = dict()
            datapoint_n[self.fields[0]] = to[0]
            datapoint_n[self.fields[1]] = to[1]
            for i, answers_key in enumerate(self.fields[2:]):
                datapoint_n[answers_key] = to[2+i] # answers starting from pos 2
            datapoints.append(datapoint_n)

        return datapoints

    def __iter__(self):
        for datapoint in self.data:
            yield (datapoint[field] for field in self.fields)

    def __len__(self):
        return len(self.data)

    def _sanity_check(self, other: KeyValueDataset):
        assert (
                self.data[0].keys() == other.data[0].keys()
        ), "You cannot do dataset operation on datasets with different keys"
        assert (
                self.task_type == other.task_type
        ), "You cannot do dataset operation on datasets for different tasks"
        assert len(self.fields) == len(
            other.fields
        ), "You cannot do dataset operation on datasets with different number fields"

    def _data2identifier(self, data: List[str]):
        id2datapoint = {}
        identifier2id = {}
        identifiers = []
        for idx, datapoint in enumerate(data):
            id2datapoint[idx] = datapoint
            # "|||" is a naive separator
            identifier = "|||".join([datapoint[field] for field in self.fields])
            identifiers.append(identifier)
            identifier2id[identifier] = idx
        identifiers = set(identifiers)  # remove duplicates
        return id2datapoint, identifier2id, identifiers

    def _identifier2data(self, id2datapoint, identifier2id, identifiers):
        result_data = []
        for identifier in identifiers:
            result_data.append(id2datapoint[identifier2id[identifier]])
        return result_data

    def __or__(self, other: KeyValueDataset) -> KeyValueDataset:
        self._sanity_check(other)
        id2datapoint, identifier2id, identifiers = self._data2identifier(
            self.data + other.data
        )
        data = self._identifier2data(id2datapoint, identifier2id, identifiers)
        return KeyValueDataset(data, self.task_type, self.fields)

    def __and__(self, other: KeyValueDataset) -> KeyValueDataset:
        self._sanity_check(other)
        id2datapoint, identifier2id, identifiers = self._data2identifier(self.data)
        _, _, identifiers2 = self._data2identifier(other.data)

        identifiers = identifiers.intersection(identifiers2)
        data = self._identifier2data(id2datapoint, identifier2id, identifiers)
        return KeyValueDataset(data, self.task_type, self.fields)

    def __sub__(self, other: KeyValueDataset) -> KeyValueDataset:
        self._sanity_check(other)
        id2datapoint, identifier2id, identifiers = self._data2identifier(self.data)
        _, _, identifiers2 = self._data2identifier(other.data)

        identifiers = identifiers.difference(identifiers2)
        data = self._identifier2data(id2datapoint, identifier2id, identifiers)
        return KeyValueDataset(data, self.task_type, self.fields)
