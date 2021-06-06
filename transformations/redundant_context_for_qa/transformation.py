from typing import Tuple, List

from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from tasks.TaskTypes import TaskType

"""
Simple perturbation to demonstrate a question answering perturbation. This perturbation repeats the context blindly
and expects the answers still to be the same. Note that this perturbation might not apply for event related tasks.
"""


class RedundantContextForQa(QuestionAnswerOperation):
    tasks = [TaskType.QUESTION_ANSWERING, TaskType.QUESTION_GENERATION]
    locales = "All"

    def __init__(self):
        super().__init__()

    def generate(self, context: str, question: str, answer: [str]) -> Tuple[str, str, List[str]]:
        context = context.rstrip() + " " + context.lstrip()
        return context, question, answer
