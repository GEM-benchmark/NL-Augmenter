from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from typing import List


class TextContainsRepetitionsFilter(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    locales = ["en"]

    def __init__(self, keywords: List[str] = None):
        super().__init__()

    def filter(self, sentence: str = None) -> bool:
        words = sentence.lower().split()
        for i in range(len(words)):
            if i > 0:
                if words[i] == words[i-1]:
                    return True
        return False

"""
if __name__ == '__main__':
    import json

    tf = TextContainsRepetitionsFilter()
    sentence = "I love cat"
    test_cases = []
    for sentence in ["I love cat",
                     "I love cat cat !!",
                     "I I want to sleep",
                     "I want to sleep",
                     "Hi hi I want to stay"]:
        test_cases.append({
            "class": tf.name(),
            "args": {},
            "inputs": {"sentence": sentence}, "outputs": tf.filter(sentence)}
        )
    json_file = {"type": "repetitions", "test_cases": test_cases}
    print(json.dumps(json_file))

    with open("test.json", "w") as out_file:
        json.dump(json_file, out_file, indent=2, ensure_ascii=True)
"""