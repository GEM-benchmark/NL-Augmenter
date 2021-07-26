import spacy
from ftlid import identify_language
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class CodeMixing(SentenceOperation):
    '''This filter is used to identify code-mixed texts in a dataset.
    It checks that there is at least one sentence in the text where there
    are tokens representing at least `k` unique languages (with at least a
    `threshold` level of confidence that the token is of that language).
    '''
    tasks = [TaskType.E2E_TASK, TaskType.TEXT_TAGGING,
             TaskType.TEXT_CLASSIFICATION]
    languages = []

    def __init__(self, k=2, threshold=0.5):
        super().__init__()
        self.nlp = spacy.load("en_core_web_sm")
        self.k = k
        self.threshold = threshold

    def filter(self, sentence: str) -> bool:
        doc = self.nlp(sentence)
        for sentence in doc.sents:
            languages = set()
            for token in sentence:
                (language,), (prob,) = identify_language(token.text,
                                                         with_prob=True)
                if prob >= self.threshold:
                    languages.add(language)
            if len(languages) >= self.k:
                return True
        return False
