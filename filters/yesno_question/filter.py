from typing import List, Tuple

import spacy

from initialize import spacy_nlp
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from tasks.TaskTypes import TaskType

"""
This filter allows to select questions that can be correctly answered with either 'yes' or 'no'.
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
        # self.nlp = spacy.load("en_core_web_sm")
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        if 'tagger' not in self.nlp.pipe_names:
            self.nlp.add_pipe("tagger", first=True)
            self.nlp.add_pipe("attribute_ruler", after="tagger")


    def filter(
        self, context: str, question: str, answers: [str]
    ) -> List[Tuple[str, str, List[str]]]:

        if question.strip()[-1] != "?":
            # It isn't a question
            return False

        doc = self.nlp(question)
        token = doc[0]
        if token.pos_ != "AUX":
            # There is no auxiliary verb
            return False

        # Everything between auxiliary and verb is the subject of the sentence
        verb_position = [
            i for i in range(len(doc)) if str(doc[i]) == token.head.text
        ][0]

        rest_of_sentence = " ".join(map(str, doc[verb_position:]))
        if "or" in rest_of_sentence:
            # This is a question about an alternative
            return False

        return True

