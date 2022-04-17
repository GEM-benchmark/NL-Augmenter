from typing import List, Tuple

from nlaugmenter.interfaces.QuestionAnswerOperation import (
    QuestionAnswerOperation,
)
from nlaugmenter.tasks.TaskTypes import TaskType

"""
Simple perturbation to demonstrate a question answering perturbation. This perturbation repeats the context blindly
and expects the answers still to be the same. Note that this perturbation might not apply for event related tasks.
"""


class RedundantContextForQa(QuestionAnswerOperation):
    tasks = [TaskType.QUESTION_ANSWERING, TaskType.QUESTION_GENERATION]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

    def generate(
        self, context: str, question: str, answers: [str]
    ) -> List[Tuple[str, str, List[str]]]:
        context = context.rstrip() + " " + context.lstrip()
        return [(context, question, answers)]


class QuestionInCaps(QuestionAnswerOperation):
    tasks = [TaskType.QUESTION_ANSWERING, TaskType.QUESTION_GENERATION]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

    def generate(
        self, context: str, question: str, answers: [str]
    ) -> List[Tuple[str, str, List[str]]]:
        return [(context, question.upper(), answers)]


"""
# Sample code to demonstrate adding test cases.

if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = RedundantContextForQa()
    test_cases = []
    context = "Steam engines are external combustion engines, where the working fluid is separate from the combustion products. " \
              "Non-combustion heat sources such as solar power, nuclear power or geothermal energy may be used."
    question = "Along with geothermal and nuclear, what is a notable non-combustion heat source?"
    answers = [
        "solar",
        "solar power",
        "solar power, nuclear power or geothermal energy"
    ]
    perturbs = tf.generate(context, question, answers)
    test_cases.append({
        "class": tf.name(),
        "inputs": {"context": context, "question": question, "answers": answers},
        "outputs": []}
    )
    for p_context, p_question, p_answers in perturbs:
        test_cases[0]["outputs"].append({"context": p_context, "question": p_question, "answers": p_answers})
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
"""
