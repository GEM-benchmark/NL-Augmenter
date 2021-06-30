import spacy
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from tasks.TaskTypes import TaskType


class QuantitativeQuestion(QuestionAnswerOperation):
    tasks = [TaskType.QUESTION_ANSWERING, TaskType.QUESTION_GENERATION]
    languages = ["en"]

    def __init__(self):
        super().__init__()
        self.nlp = spacy.load("en_core_web_sm")
        # Covers the broad types of quant questions: distance , age , measurable , un-measurable
        self.quant_ques = ['many','far','close','long','much','old']

    def filter(self,context:str = None,question: str = None,answers:str = None) -> bool:
        tokenized = self.nlp(question, disable=["parser", "tagger", "ner"])
        if 'how' == tokenized[0].text.lower() and tokenized[1].text.lower() in self.quant_ques:
            return True
        else:
            return False



