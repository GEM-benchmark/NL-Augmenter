import spacy
from typing import Tuple, List

from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from tasks.TaskTypes import TaskType
from typing import List

"""
A filter on text length (number of tokens).
"""


class YesNoQuestionFilter(QuestionAnswerOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.QUESTION_ANSWERING,
        TaskType.QUESTION_GENERATION,
    ]
    languages = ["en"]

    def __init__(self):
        super().__init__()
        self.nlp = spacy.load("en_core_web_sm")

    def filter(
        self, context: str, question: str, answers: [str]
    ) -> List[Tuple[str, str, List[str]]]:

        if question.strip()[-1] != "?":
            return False

        if " or " in question:
            return False

        doc = self.nlp(question)
        token = doc[0]
        if token.pos_ != "AUX":
            return False

        return True


if __name__ == "__main__":
    import json
    from TestRunner import convert_to_snake_case

    tf = YesNoQuestionFilter()

    test_cases = []
    for i, sentence in enumerate(
        [
            "Wasn't she angry when you told her about the accident?",
            "Have you got an identity card?",
            "Would you rather drink tea or a coffee?",
            "Would you like some soup?",
            "Should you need something, I will be in my room",
        ]
    ):
        res = tf.filter("", sentence, [])
        print(res)
        test_cases.append(
            {
                "class": tf.name(),
                "inputs": {"context": "", "question": sentence, "answers": []},
                "outputs": res,
            }
        )

    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
