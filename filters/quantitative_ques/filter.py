import spacy
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from tasks.TaskTypes import TaskType


class QuantitativeQuestion(QuestionAnswerOperation):
    '''
    This filter used to identify the quantitative questions in a dataset
    It identifies the commonly used quant questions based on lexical matching
    (The set of phrases are stored in the self.quant_ques)
    '''
    tasks = [TaskType.QUESTION_ANSWERING, TaskType.QUESTION_GENERATION]
    languages = ["en"]

    def __init__(self):
        super().__init__()
        self.nlp = spacy.load("en_core_web_sm")
        # Covers the broad types of quant questions: distance , age , measurable , un-measurable
        self.quant_ques = ['many','much',
                           'close','far',
                           'young','old',
                           'short','tall',
                           'heavy','light',
                           'narrow','wide',
                           'deep','shallow',
                           'broad','thin',
                           'near','long']


    def filter(self,context:str = None,question: str = None,answers:str = None) -> bool:
        tokenized = self.nlp(question, disable=["parser", "tagger", "ner"])
        return ('how' == tokenized[0].text.lower() and tokenized[1].text.lower() in self.quant_ques)


