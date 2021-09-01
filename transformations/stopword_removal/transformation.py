from nltk.corpus import stopwords
from nltk.tokenize import ToktokTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def stopword_remove(text, max_outputs=1):
    """
    Remove stopwords using standard list comprehension.
    Assumes that user_input text is in the English language.
    Every string in the user_input is detokenized.
    Returns a tokenized version of the text with stopwords removed.
    """
    stop_words = set(stopwords.words('english'))
    text_tokenized = ToktokTokenizer().tokenize(text)
    return TreebankWordDetokenizer().detokenize([word for word in text_tokenized if word.lower() not in stop_words])

class StopwordRemoval(SentenceOperation):
    """
      This class offers a method for a stopword removal function to transform
      the text. Stopword removal is the process of removing stopwords from a text.
      The library of stopwords chosen is based on NLTK's library of stopwords.
    """
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]
    heavy = True

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

    def generate(self, raw_text: str):
        pertubed_text = stopword_remove(
            text=raw_text,
            max_outputs=self.max_outputs
        )
        return pertubed_text