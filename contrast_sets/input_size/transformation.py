from collections import defaultdict

from interfaces.ContrastSetTransformation import ContrastSetTransformation
from tasks.TaskTypes import TaskType


class InputSize(ContrastSetTransformation):

    tasks = [TaskType.E2E_TASK]
    locales = ["en"]

    def generate(self, dataset: dict, field_name: str) -> dict:
        if isinstance(dataset, dict):
            return {self.name(): self.input_size(dataset, field_name)}

    def input_size(self, dataset, field_name):
        "Compare items with different input sizes."
        contrast_set = defaultdict(list)
        for entry in dataset['test']:
            input_field = entry[field_name]
            if isinstance(input_field, str):
                input_field = input_field.split(', ')
            contrast_set[f"input_length_{len(input_field)}"].append(entry['gem_id'])
        return contrast_set


