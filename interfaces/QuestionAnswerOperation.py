from typing import Tuple, List

from interfaces.Operation import Operation


class QuestionAnswerOperation(Operation):
    """
    The base class for implementing question answering style perturbations and transformations.

    "tasks" :: The tasks for which this perturbation is applicable. All the list of tasks are
    given in tasks.TaskType.

    "languages" :: The locales and/or languages for which these perturbation are applicable. eg. "es",
    "mr","en_IN". If the context, question and answer are in separate locales, the implementation can
    accordingly override the domain(cls) function.
    """

    def generate(
        self, context: str, question: str, answers: [str]
    ) -> Tuple[str, str, List[str]]:
        raise NotImplementedError

    def filter(self, context: str, question: str, answers: [str]) -> bool:
        raise True
